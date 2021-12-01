package com.sjtu.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@TableName(value = "image")
@Data
@AllArgsConstructor
@NoArgsConstructor
public class Image {
    @TableId(value = "id")
    private String id;
    private String name;
    private String version;
    private String information;  //信息介绍
    private String tag;    //标签
    private String userId;
}
