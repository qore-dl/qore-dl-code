package com.sjtu.shiro;

import com.alibaba.fastjson.JSONObject;
import com.auth0.jwt.exceptions.TokenExpiredException;
import com.sjtu.common.Constant;
import com.sjtu.entity.User;
import com.sjtu.service.UserService;
import com.sjtu.utils.JwtUtil;
import com.sjtu.utils.RedisUtil;
import org.apache.shiro.authc.AuthenticationException;
import org.apache.shiro.authc.AuthenticationInfo;
import org.apache.shiro.authc.AuthenticationToken;
import org.apache.shiro.authc.SimpleAuthenticationInfo;
import org.apache.shiro.authz.AuthorizationInfo;
import org.apache.shiro.authz.SimpleAuthorizationInfo;
import org.apache.shiro.realm.AuthorizingRealm;
import org.apache.shiro.subject.PrincipalCollection;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Lazy;

//该realm并不用于登录，而是登录后的请求认证
public class JwtRealm extends AuthorizingRealm {

    @Lazy
    @Autowired
    private UserService userService;
    @Lazy
    @Autowired
    private RedisUtil redisUtil;

    public JwtRealm(){};

    @Override
    public boolean supports(AuthenticationToken token) {
        return token instanceof JwtToken;
    }

   /*主要用于请求认证*/
    @Override
    protected AuthenticationInfo doGetAuthenticationInfo(AuthenticationToken auth) throws AuthenticationException {
        String token = (String) auth.getCredentials();
        if (null == token) {
            throw new AuthenticationException("token为空!");
        }
        // 解密获得user_id，用于和数据库进行对比
        String user_id = JwtUtil.getClaim(token,Constant.ID);
        if(null == user_id){
            throw new AuthenticationException("Token无法解析出用户");
        }
        User user = userService.getUserById(user_id);
        if (null == user) {
            throw new AuthenticationException("用户不存在!");
        }
        /*当前账号请求在过渡时间内，直接放行*/
        if(redisUtil.hasKey(Constant.PREFIX_SHIRO_REFRESH_TOKEN_TRANSITION+user_id)){
            String old_access_token = redisUtil.get(Constant.PREFIX_SHIRO_REFRESH_TOKEN_TRANSITION+user_id).toString();
            if(token.equals(old_access_token)){
                return new SimpleAuthenticationInfo(user, old_access_token, getName());
            }
        }
        /*当前的token有效，并且redis里有refreshToken*/
        if(JwtUtil.verify(token,user_id) && redisUtil.hasKey(Constant.PREFIX_SHIRO_REFRESH_TOKEN + user_id)){
            String currentTimeMillisRedis = redisUtil.get(Constant.PREFIX_SHIRO_REFRESH_TOKEN + user_id).toString();
            // 获取AccessToken时间戳，与RefreshToken的时间戳对比
            if (JwtUtil.getClaim(token, Constant.CURRENT_TIME_MILLIS).equals(currentTimeMillisRedis)) {
                /*实际上，这里之后的比较没有意义，所有有效的比较都在该语句前面*/
                return new SimpleAuthenticationInfo(user, token, getName());
            }
        }
        throw new TokenExpiredException("Token expired or incorrect");   //不放进全局处理
    }

    //授权
    @Override
    protected AuthorizationInfo doGetAuthorizationInfo(PrincipalCollection principalCollection) {
        SimpleAuthorizationInfo info = new SimpleAuthorizationInfo();
        User user = (User) principalCollection.getPrimaryPrincipal();
        JSONObject auth = user.getAuthority();
        for(String keys : auth.keySet()){
            if((Boolean) auth.get(keys)){
                info.addStringPermission(keys);
            }
        }
        return info;
    }
}
