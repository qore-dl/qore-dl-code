package com.sjtu.service;

import com.sjtu.entity.ResetPassword;

import java.util.Date;

public interface ResetPasswordService {
    /*通过user_id获取其修改密码的信息*/
    ResetPassword getOneByUserId(String user_id);
    /*插入一条记录*/
    Boolean insertResetPwd(ResetPassword resetPassword);
    /*更新一条记录*/
    Boolean updateResetPwd(ResetPassword resetPassword);
    /*判断当前时间是否在发送验证码的冷却期间*/
    Boolean isEnableResetPwd(Date now_time, ResetPassword resetPassword);
    /*判断是否超过当日修改次数*/
    Boolean isLimitResetPwd(ResetPassword resetPassword);
}
