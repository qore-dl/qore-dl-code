package com.sjtu.service;

import com.sjtu.common.Response;
import com.sjtu.entity.User;

public interface UserService {
    /*登录:登录名（用户名或者邮箱）+密码*/
    Response Login(String LoginName,String password);
    /*注册:用户名+密码+邮箱（用户名与密码必须检测是否已经注册过）*/
    Response Register(String username,String password,String email,String role);
    /*用户账户激活*/
    Response Activate(String code);
    /*通过用户名找用户*/
    User getUserByName(String username);
    /*通过邮箱找用户，注册时邮箱必须不可以重复*/
    User getUserByEmail(String email);
    /*通过用户id获取用户*/
    User getUserById(String id);
    /*发送重置密码的验证码*/
    Response resetPassword_Mail(String sendTo);
    /*检查code有效性+重置密码*/
    Response resetPassword(String sendTo, String code, String password);
    /*退出登录*/
    Response Logout(String token);
}
