package com.sjtu.service.impl;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.sjtu.common.Constant;
import com.sjtu.common.Response;
import com.sjtu.common.StatusCode;
import com.sjtu.entity.ResetPassword;
import com.sjtu.entity.User;
import com.sjtu.exception.ServiceException;
import com.sjtu.mapper.UserMapper;
import com.sjtu.service.ResetPasswordService;
import com.sjtu.service.UserService;
import com.sjtu.utils.*;
import org.apache.shiro.SecurityUtils;
import org.apache.shiro.authc.UsernamePasswordToken;
import org.apache.shiro.subject.Subject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.HashMap;
import java.util.Map;

@Service
public class UserServiceImpl implements UserService {
    private static final Logger logger = LoggerFactory.getLogger(UserServiceImpl.class);
    @Autowired
    UserMapper userMapper;
    @Autowired
    ResetPasswordService resetPasswordService;
    @Autowired
    RedisUtil redisUtil;
    @Autowired
    MailUtil mailUtil;
    //创建用户id
    IdUtil create_user_id = new IdUtil(0,0);

    @Override
    public Response Login(String LoginName, String password) {
        Subject subject = SecurityUtils.getSubject();
        UsernamePasswordToken usernamePasswordToken = new UsernamePasswordToken(LoginName,password);
        subject.login(usernamePasswordToken);
        //认证通过
        User user = (User)subject.getPrincipal();
        String token = getToken(user);
        Map<String,String> data = new HashMap<>();
        data.put("Token",token);
        return new Response(StatusCode.SUCCESS,"登录成功",data);
    }

    @Override
    public Response Register(String username, String password, String email, String role) {
        //判断用户名是否重复
        User user = getUserByName(username);
        if(user!=null){
            return new Response(StatusCode.FAIL_REGISTER,"用户名已被占用");
        }
        //邮箱是否合法
        if(!email.matches("^\\w+@(\\w+\\.)+\\w+$")){
            return new Response(StatusCode.FAIL_REGISTER,"邮箱不合法");
        }
        //判断邮箱是否重复
        User user1 = getUserByEmail(email);
        if(user1!=null){
            return new Response(StatusCode.FAIL_REGISTER,"该邮箱已被注册");
        }
        //密码加密，写入数据库
        User user2 = new User();
        String salt = PasswordSaltUtil.randomAlphanumeric(5);
        user2.setId(create_user_id.generateNextId());
        user2.setName(username);
        user2.setEmail(email);
        user2.setSalt(salt);
        user2.setPassword(PasswordSaltUtil.md5(password,salt));
        user2.setActivation(0);   //未激活
        user2.setRole(role);
        if(user2.getRole().equals("user")){
            user2.setAuthority(JSONObject.parseObject(JSON.toJSONString(Constant.USER_AUTHORITY)));
        }else{
            user2.setAuthority(JSONObject.parseObject(JSON.toJSONString(Constant.ADMIN_AUTHORITY)));
        }
        //发送激活邮件
        String code = JwtUtil.createToken(user2.getId(), String.valueOf(System.currentTimeMillis()));
        String title = "账户激活——智能计算服务平台";
        String content = "<html>\n" +
                "<body>\n" +
                "<p>" + "尊敬的" + user2.getName() + "，您好" + "<br/>" + "这里是智能计算服务平台<br/>" +
                "请点击以下网址进行邮箱认证:<br/>" +
                "<a style=\"font-size:20px; color: #409EFF\" href=\"http://172.16.20.190:5052/activate?code="+code+"\">http://172.16.20.190:5052/activate?code=" + code + "</a>" +
                "<br/>请在5分钟之内进行认证" +
                "<br/>如果非本人操作，请忽略本邮件，如有疑问，欢迎致信2963148486@qq.com" +
                "</p>" +
                "</body>\n" +
                "</html>\n";
        try {
            mailUtil.sendMimeMail(user2.getEmail(),title,content);
            redisUtil.set(user2.getId(),code,Constant.LINK_EXPIRE_TIME/1000);    //控制链接的有效时间
        } catch (Exception e) {
            throw new ServiceException(StatusCode.FAIL_REGISTER,"该邮箱不存在");
        }
        int row = userMapper.insert(user2);
        if(row>0){
            return new Response(StatusCode.SUCCESS,"注册成功，请尽快前往邮箱激活该账户",user2.getId());
        }
        return new Response(StatusCode.FAIL_REGISTER,"注册失败");
    }

    @Override
    public Response Activate(String code) {
        String user_id = JwtUtil.getClaim(code,Constant.ID);
        User user = userMapper.selectById(user_id);
        if(user!=null && redisUtil.hasKey(user_id)){
            user.setActivation(1);
            int row = userMapper.updateById(user);
            if(row>0){
                return new Response(StatusCode.SUCCESS,"用户激活成功");
            }
        }
        return new Response(StatusCode.FAIL_ACTIVATE,"用户激活失败");
    }

    @Override
    public User getUserByName(String username) {
        return userMapper.selectOne(new QueryWrapper<User>().eq("name",username));
    }

    @Override
    public User getUserByEmail(String email) {
        return userMapper.selectOne(new QueryWrapper<User>().eq("email",email));
    }

    @Override
    public User getUserById(String id) {
        return userMapper.selectById(id);
    }

    @Override
    public Response resetPassword_Mail(String sendTo) {
        User user = getUserByEmail(sendTo);
        if(user==null){
            return new Response(StatusCode.NOT_FOUND,"该邮箱并未注册");
        }
        String code = mailUtil.create_code(6);
        Date currentTime = new Date();
        Date end_time = new Date(currentTime.getTime() + 5*60*1000);
        //判断之前是否重置过密码(仅限邮件重置)
        ResetPassword resetPassword = resetPasswordService.getOneByUserId(user.getId());
        if(resetPassword!=null){
            //这次发送验证码距离上次发送超过指定时间，即可发送
            if(resetPasswordService.isEnableResetPwd(currentTime,resetPassword)){
                if(resetPasswordService.isLimitResetPwd(resetPassword)){
                    resetPassword.setCode(code);
                    resetPassword.setCreateTime(currentTime);
                    resetPassword.setEndTime(end_time);
                    resetPassword.setResetNum(resetPassword.getResetNum()+1);
                    if(!resetPasswordService.updateResetPwd(resetPassword)){
                        //更新重置密码表
                        logger.error("更新数据库失败——密码重置表");
                    }
                }else{
                    return new Response(StatusCode.FAIL_RESET_PWD,"今日修改次数已超过上限，请明日再来");
                }
            }else{
                return new Response(StatusCode.FAIL_RESET_PWD,"距离上次发送验证码时间间隔未超过一小时，请等待~");
            }
        }else{
            ResetPassword resetPassword1 = new ResetPassword();
            resetPassword1.setUserId(user.getId());
            resetPassword1.setCode(code);
            resetPassword1.setCreateTime(currentTime);
            resetPassword1.setEndTime(end_time);
            resetPassword1.setResetNum(1);
            if(!resetPasswordService.insertResetPwd(resetPassword1)){
                //插入密码重置表
                logger.error("插入数据库失败——密码重置表");
            }
        }
        //发送验证码
        String title = "重置密码——智能计算服务平台";
        String content = "<html>\n" +
                "<body>\n" +
                "<p>" + "尊敬的" + user.getName() + "，您好" + "<br/>" + "你正在智能计算服务平台进行重置密码操作<br/>" +
                "您本次重置密码的验证码为<br/>" +
                "<p style=\"font-size:24px; color: #409EFF\">" + code +"</p>" +
                "<br/>请在5分钟之内填写验证码" +
                "<br/>如果非本人操作，请忽略本邮件，如有疑问，欢迎致信2963148486@qq.com" +
                "</p>" +
                "</body>\n" +
                "</html>\n";

        try {
            mailUtil.sendMimeMail(sendTo,title,content);
            return new Response(StatusCode.SUCCESS,"邮件发送成功，验证码的有效期为5分钟");
        } catch (Exception e) {
            throw new ServiceException(StatusCode.FAIL_RESET_PWD,"邮件发送失败");
        }
    }

    @Override
    public Response resetPassword(String sendTo, String code, String password) {
        User user = getUserByEmail(sendTo);
        if(user==null){
            return new Response(StatusCode.FAIL_RESET_PWD,"该邮箱并未注册");
        }
        //检查code的有效性
        Date currentTime = new Date();
        ResetPassword resetPassword = resetPasswordService.getOneByUserId(user.getId());
        if(resetPassword.getCode().equals(code)){
            if(currentTime.before(resetPassword.getEndTime())){
                String salt = PasswordSaltUtil.randomAlphanumeric(5);   //生成新的盐值
                String md5Password = PasswordSaltUtil.md5(password,salt);
                user.setPassword(md5Password);
                user.setSalt(salt);
                int row = userMapper.updateById(user);
                if(row>0){
                    return new Response(StatusCode.SUCCESS,"密码重置成功，请前往登录页面");
                }
            }else{
                return new Response(StatusCode.FAIL_RESET_PWD,"验证码已过期，请等待一段时间再重新获取");
            }
        }else{
            return new Response(StatusCode.FAIL_RESET_PWD,"验证码错误");
        }
        return new Response(StatusCode.FAIL_RESET_PWD,"密码重置失败");
    }

    @Override
    public Response Logout(String token) {
        String user_id = JwtUtil.getClaim(token,Constant.ID);
        String key = Constant.PREFIX_SHIRO_REFRESH_TOKEN + user_id;
        redisUtil.del(key);
        return new Response(StatusCode.SUCCESS,"成功退出登录");
    }

    /*根据用户获取token，用于登录后的api请求鉴权*/
    private String getToken(User user){
        //当前时间戳
        String currentTimeMillis = String.valueOf(System.currentTimeMillis());
        String token = JwtUtil.createToken(user.getId(), currentTimeMillis);
        redisUtil.set(Constant.PREFIX_SHIRO_REFRESH_TOKEN + user.getId(),currentTimeMillis,Constant.REFRESH_EXPIRE_TIME/1000);
        return token;
    }
}
