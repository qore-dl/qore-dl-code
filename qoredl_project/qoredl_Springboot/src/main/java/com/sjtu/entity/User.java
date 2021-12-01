package com.sjtu.entity;

import com.alibaba.fastjson.JSONObject;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import com.baomidou.mybatisplus.extension.handlers.FastjsonTypeHandler;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/*用户实体类*/
@TableName(value = "user",autoResultMap = true)
@Data
@AllArgsConstructor
@NoArgsConstructor
public class User {
    @TableId(value = "id")
    private String id;
    private String name;
    private String password;
    private String email;    //主要用于后期的找回密码
    private String salt;    //密码加密的盐值
    private int activation;   //是否激活
    private String role;    //0代表普通用户，1代表管理员
    @TableField(typeHandler = FastjsonTypeHandler.class)
    private JSONObject authority;   //权限
}
