package com.sjtu.controller;

import com.sjtu.common.Response;
import com.sjtu.common.StatusCode;
import com.sjtu.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;
import java.util.Map;


/*用户操作的一些接口*/
@RestController
public class UserController {
    @Autowired
    UserService userService;

    /*未通过请求认证的跳转接口*/
    @GetMapping("/unauthenticated")
    public Response unauthenticated(){
        return new Response(StatusCode.TOKEN_EXPIRED,"未通过请求认证");
    }

    /*用户登录接口*/
    @PostMapping("/Login")
    public Response Login(@RequestBody Map<String,String> map){
        return userService.Login(map.get("LoginName"),map.get("password"));
    }

    /*用户注册接口*/
    @PostMapping("/Register")
    public Response Register(@RequestBody Map<String,String> map){
        return userService.Register(map.get("username"),map.get("password"),map.get("email"),map.get("role"));
    }

    /*用户注册邮箱验证接口*/
    @PostMapping("/activate")
    public Response checkCode(@RequestBody Map<String,String> map){
        return userService.Activate(map.get("code"));
    }

    /*获取重置密码的验证码*/
    @PostMapping("/getVerifyCode")
    public Response getVerifyCode(@RequestBody Map<String,String> map){
        return userService.resetPassword_Mail(map.get("sendTo"));
    }

    /*密码重置确认——登录页面 邮件重置*/
    @PostMapping("/resetPassword")
    public Response resetPassword(@RequestBody Map<String,String> map){
        return userService.resetPassword(map.get("sendTo"),map.get("code"),map.get("password"));
    }

    /*退出登录*/
    @PostMapping("/Logout")
    public Response Logout(HttpServletRequest request){
        return userService.Logout(request.getHeader("Token"));
    }
}
