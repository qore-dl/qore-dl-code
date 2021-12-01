package com.sjtu.service;

import com.sjtu.common.Response;
import org.springframework.web.multipart.MultipartFile;

import javax.servlet.http.HttpServletRequest;
import java.util.Map;

public interface TaskService {
    /*提交任务*/
    Response submitTask(Map<String,Object> map, HttpServletRequest request);
    /*获取Train_config*/
    Response getTrainConfigList();
    /*删除任务(运行中的不可删除)*/
    Response deleteTask(String name);
    /*获取所有的任务信息*/
    Response getTaskList();
    /*根据任务名获取任务信息*/
    Response getTaskByName(String name);
    /*调整任务资源*/
    Response adjustTask(Map<String,String> map);
    /*根据用户id获取任务列表   管理员*/
    Response getTaskByUserId(String id);
    /*用户获取其任务列表*/
    Response getUserTaskList();
    /*用户获取其任务信息*/
    Response getUserTaskByName(String name);
    /*上传train_config文件*/
    Response upload_train_config(MultipartFile file);
    /*删除train_config文件*/
    Response delete_train_config(String name);

}
