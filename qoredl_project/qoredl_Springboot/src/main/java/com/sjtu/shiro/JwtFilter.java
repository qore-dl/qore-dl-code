package com.sjtu.shiro;

import com.auth0.jwt.exceptions.TokenExpiredException;
import com.sjtu.common.Constant;
import com.sjtu.utils.JwtUtil;
import com.sjtu.utils.RedisUtil;
import lombok.extern.slf4j.Slf4j;
import org.apache.shiro.web.filter.authc.BasicHttpAuthenticationFilter;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.context.WebApplicationContext;
import org.springframework.web.context.support.WebApplicationContextUtils;

import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

/*
 * 拦截鉴权
 */
@Slf4j
public class JwtFilter extends BasicHttpAuthenticationFilter {

    @Override
    protected boolean isAccessAllowed(ServletRequest request, ServletResponse response, Object mappedValue) {
        try {
            executeLogin(request, response);
            return true;
        } catch (Exception e) {
            Throwable throwable = e.getCause();
            if(throwable instanceof TokenExpiredException){
                if(this.RefreshToken(request,response)){
                   return true;
                }
            }
            //认证失败
            this.unauthenticated(response);
            return false;
        }
    }
    //执行login方法，实现请求认证
    @Override
    protected boolean executeLogin(ServletRequest request, ServletResponse response) {
        HttpServletRequest httpServletRequest = (HttpServletRequest) request;
        String authorization = httpServletRequest.getHeader("Token");
        JwtToken token = new JwtToken(authorization);
        // 提交给realm进行登入，如果错误他会抛出异常并被捕获
        getSubject(request, response).login(token);
        return true;
    }
    /**
     * 认证失败 跳转到 /unauthorized
     */
    private void unauthenticated(ServletResponse resp) {
        try {
            HttpServletResponse httpServletResponse = (HttpServletResponse) resp;
            httpServletResponse.sendRedirect("/unauthenticated");
        } catch (IOException e) {
            log.error(e.getMessage());
        }
    }

    public <T> T getBean(Class<T> clazz,HttpServletRequest request){
        WebApplicationContext applicationContext = WebApplicationContextUtils.getRequiredWebApplicationContext(request.getServletContext());
        return applicationContext.getBean(clazz);
    }

    /*accessToken刷新，如果refreshToken未过期，则刷新返回新的accessToken*/
    private Boolean RefreshToken(ServletRequest request, ServletResponse response){

        HttpServletRequest httpServletRequest = (HttpServletRequest) request;
        RedisUtil redisUtil = getBean(RedisUtil.class,httpServletRequest);
        String access_token = httpServletRequest.getHeader("Token");
        String user_id = JwtUtil.getClaim(access_token,Constant.ID);
        String refreshTokenKey = Constant.PREFIX_SHIRO_REFRESH_TOKEN + user_id;
        /*多个并发请求到达这，必须加锁，使得后面的task与redis的时间戳必然不同*/
        synchronized(this){
            if(redisUtil.hasKey(refreshTokenKey)){
                //判断时间戳
                String currentTimeMillisRedis = redisUtil.get(refreshTokenKey).toString();
                if(JwtUtil.getClaim(access_token,Constant.CURRENT_TIME_MILLIS).equals(currentTimeMillisRedis)){
                    // 设置RefreshToken中的时间戳为当前最新时间戳
                    String currentTimeMillis = String.valueOf(System.currentTimeMillis());
                    redisUtil.set(refreshTokenKey, currentTimeMillis, Constant.REFRESH_EXPIRE_TIME/1000);

                    // 刷新AccessToken，为当前最新时间戳
                    String new_access_token = JwtUtil.createToken(user_id, currentTimeMillis);

                    // 使用AccessToken 再次提交给ShiroRealm进行认证，如果没有抛出异常则登入成功，返回true
                    this.getSubject(request, response).login(new JwtToken(new_access_token));
                    //防止token并发问题,保存旧token
                    redisUtil.set(Constant.PREFIX_SHIRO_REFRESH_TOKEN_TRANSITION + user_id,access_token,Constant.REFRESH_TRANSITION_EXPIRE_TIME/1000);
                    // 设置响应的Header头新Token
                    HttpServletResponse httpServletResponse = (HttpServletResponse) response;
                    httpServletResponse.setHeader("Token", new_access_token);
                    httpServletResponse.setHeader("Access-Control-Expose-Headers", "Token");
                    return true;
                }else{
                    /*说明该请求在刷新token之后到达，判断其是否在过渡时间内*/
                    String old_token_key = Constant.PREFIX_SHIRO_REFRESH_TOKEN_TRANSITION + user_id;
                    if(redisUtil.hasKey(old_token_key)){
                        String old_access_token = redisUtil.get(old_token_key).toString();
                        //判断token是否一致
                        if(access_token.equals(old_access_token)){
                            this.getSubject(request,response).login(new JwtToken(old_access_token));
                            return true;
                        }
                    }
                }
            }
        }
        return false;
    }

    /**
     * 对跨域提供支持
     */
    @Override
    protected boolean preHandle(ServletRequest request, ServletResponse response) throws Exception {
        HttpServletRequest httpServletRequest = (HttpServletRequest) request;
        HttpServletResponse httpServletResponse = (HttpServletResponse) response;
        // 标识允许哪个域到请求，直接修改成请求头的域
        httpServletResponse.setHeader("Access-control-Allow-Origin", httpServletRequest.getHeader("Origin"));
        // 标识允许的请求方法
        httpServletResponse.setHeader("Access-Control-Allow-Methods", "GET,POST,OPTIONS,PUT,DELETE");
        // 响应首部 Access-Control-Allow-Headers 用于 preflight request （预检请求）中，列出了将会在正式请求的 Access-Control-Expose-Headers 字段中出现的首部信息。修改为请求首部
        httpServletResponse.setHeader("Access-Control-Allow-Headers", httpServletRequest.getHeader("Access-Control-Request-Headers"));
        //给option请求直接返回正常状态
        if (httpServletRequest.getMethod().equals(RequestMethod.OPTIONS.name())) {
            httpServletResponse.setStatus(HttpStatus.OK.value());
            return false;
        }
        return super.preHandle(request, response);
    }

}
