package com.sjtu.controller;

import com.sjtu.common.Response;
import com.sjtu.service.TaskService;
import org.apache.shiro.authz.annotation.Logical;
import org.apache.shiro.authz.annotation.RequiresPermissions;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import javax.servlet.http.HttpServletRequest;
import java.util.Map;

@RestController
public class TaskController {
    @Autowired
    TaskService taskService;

    @PostMapping("/submitTask")
    @RequiresPermissions(value = {"user:submitTask","admin:submitTask"},logical = Logical.OR)
    public Response submitTask(@RequestBody Map<String,Object> map, HttpServletRequest request){
        return taskService.submitTask(map,request);
    }

    @GetMapping("/getTrainConfigList")
    @RequiresPermissions(value = {"user:getTrainConfigList","admin:getTrainConfigList"},logical = Logical.OR)
    public Response getTrainConfigList(){
        return taskService.getTrainConfigList();
    }

    @PostMapping("/deleteTask")
    @RequiresPermissions(value = {"user:deleteTask","admin:deleteTask"},logical = Logical.OR)
    public Response deleteTask(@RequestBody Map<String,String> map){
        return taskService.deleteTask(map.get("job_name"));
    }

    @GetMapping("/getTaskList")
    @RequiresPermissions(value = {"admin:getTaskList"})
    public Response getTaskList(){
        return taskService.getTaskList();
    }

    @PostMapping("/getTaskByName")
    @RequiresPermissions(value = {"admin:getTaskByName"})
    public Response getTaskByName(@RequestBody Map<String,String> map){
        return taskService.getTaskByName(map.get("job_name"));
    }

    @GetMapping("/getUserTaskList")
    @RequiresPermissions(value = {"user:getUserTaskList"})
    public Response getUserTaskList(){
        return taskService.getUserTaskList();
    }

    @PostMapping("/getUserTaskByName")
    @RequiresPermissions(value = {"user:getUserTaskByName"})
    public Response getUserTaskByName(@RequestBody Map<String,String> map){
        return taskService.getUserTaskByName(map.get("job_name"));
    }

    @PostMapping("/adjustTask")
    @RequiresPermissions(value = {"admin:adjustTask","user:adjustTask"}, logical = Logical.OR)
    public Response adjustTask(@RequestBody Map<String,String> map){
        return taskService.adjustTask(map);
    }

    @PostMapping("/uploadTrainConfig")
    @RequiresPermissions(value = {"admin:uploadTrainConfig","user:uploadTrainConfig"},logical = Logical.OR)
    public Response uploadTrainConfig(@RequestParam("file") MultipartFile file){
        return taskService.upload_train_config(file);
    }

    @PostMapping("/deleteTrainConfig")
    @RequiresPermissions(value = {"admin:deleteTrainConfig","user:deleteTrainConfig"},logical = Logical.OR)
    public Response deleteTrainConfig(@RequestBody Map<String,String> map){
        return taskService.delete_train_config(map.get("config_file_name"));
    }
}
