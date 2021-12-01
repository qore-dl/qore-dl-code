package com.sjtu.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.sjtu.common.Constant;
import com.sjtu.entity.ResetPassword;
import com.sjtu.mapper.ResetPasswordMapper;
import com.sjtu.service.ResetPasswordService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Date;

@Service
public class ResetPasswordServiceImpl implements ResetPasswordService {

    @Autowired
    ResetPasswordMapper resetPasswordMapper;

    @Override
    public ResetPassword getOneByUserId(String user_id) {
        return resetPasswordMapper.selectOne(new QueryWrapper<ResetPassword>().eq("user_id",user_id));
    }

    @Override
    public Boolean insertResetPwd(ResetPassword resetPassword) {
        int row = resetPasswordMapper.insert(resetPassword);
        if(row>0){
            return true;
        }
        return false;
    }

    @Override
    public Boolean updateResetPwd(ResetPassword resetPassword) {
        int row = resetPasswordMapper.updateById(resetPassword);
        if(row>0){
            return true;
        }
        return false;
    }

    @Override
    public Boolean isEnableResetPwd(Date now_time, ResetPassword resetPassword) {
        //超过上一次修改密码1个小时即可再次修改
        if(now_time.after(new Date(resetPassword.getCreateTime().getTime() + 60*60*1000))){
            return true;
        }
        return false;
    }

    @Override
    public Boolean isLimitResetPwd(ResetPassword resetPassword) {
        if(resetPassword.getResetNum() < Constant.RESET_PASSWORD_LIMIT_TIME){
            return true;
        }
        //判断当前时间距离上一次修改密码时间是否超过24小时，是则重置今日可修改次数
        Date currentTime = new Date();
        if(currentTime.after(new Date(resetPassword.getCreateTime().getTime() + 24*60*60*1000))){
            resetPassword.setResetNum(0);
            resetPasswordMapper.updateById(resetPassword);
            return true;
        }
        return false;
    }
}
