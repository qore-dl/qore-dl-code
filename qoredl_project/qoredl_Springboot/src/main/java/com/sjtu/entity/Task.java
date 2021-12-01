package com.sjtu.entity;

import com.alibaba.fastjson.JSONObject;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import com.baomidou.mybatisplus.extension.handlers.FastjsonTypeHandler;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@TableName(value = "task")
@Data
@AllArgsConstructor
@NoArgsConstructor
public class Task {
    @TableId(value = "id")
    private String id;
    private String name;
    private String information;
    private String startTime;
    private String endTime;
    private String userId;
    private int status;    //-1表示未运行  0表示运行完成  1表示运行中
    private String resource;   //资源使用量
}
