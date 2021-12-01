package com.sjtu.service.impl;

import com.alibaba.fastjson.JSONObject;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.conditions.update.UpdateWrapper;
import com.sjtu.common.Constant;
import com.sjtu.common.Response;
import com.sjtu.common.StatusCode;
import com.sjtu.entity.Task;
import com.sjtu.mapper.TaskMapper;
import com.sjtu.service.TaskService;
import com.sjtu.utils.IdUtil;
import com.sjtu.utils.InputStreamUtil;
import com.sjtu.utils.JwtUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import javax.servlet.http.HttpServletRequest;
import java.io.IOException;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;


@Service
public class TaskServiceImpl implements TaskService {
    @Autowired
    TaskMapper taskMapper;

    IdUtil create_task_id  = new IdUtil(2,2);

    @Override
    public Response submitTask(Map<String,Object> map, HttpServletRequest request) {
        String taskInformation = map.get("information").toString();
        //调用接口
        RestTemplate restTemplate = new RestTemplate();
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<Map> requestBody = new HttpEntity<>(JSONObject.parseObject(JSONObject.toJSONString(map.get("data")), Map.class),headers);
        Response res = restTemplate.postForEntity(Constant.SUBMIT_TASK_URL,requestBody,Response.class).getBody();
        assert res != null;
        if(res.getCode().equals("0")) {
            //插入数据库
            String token = request.getHeader("Token");
            String taskName = ((LinkedHashMap)res.getData()).get("name").toString();
            String userId = JwtUtil.getClaim(token, "id");
            String resource = JSONObject.toJSONString(map.get("resource"));
            Task task = new Task();
            task.setId(create_task_id.generateNextId());
            task.setName(taskName);
            task.setInformation(taskInformation);
            //设置任务的资源使用情况
            task.setResource(resource);
            task.setUserId(userId);
            //确保任务名的不重复
            QueryWrapper<Task> wrapper = new QueryWrapper<>();
            wrapper.eq("name", taskName);
            List<Task> list = taskMapper.selectList(wrapper);
            if (list.size() != 0) {
                return new Response(StatusCode.FAIL_SUBMIT, "任务名重复");
            }
            //插入数据库
            int row = taskMapper.insert(task);
            if (row > 0) {
                return new Response(StatusCode.SUCCESS, "运行成功", res.getData());
            } else {
                return new Response(StatusCode.FAIL_SUBMIT, "运行失败");
            }
        }
        return new Response(StatusCode.FAIL_SUBMIT,"运行失败");
    }

    @Override
    public Response getTrainConfigList() {
        RestTemplate restTemplate = new RestTemplate();
        Response data = restTemplate.getForEntity(Constant.GET_CONFIG_URL,Response.class).getBody();
        assert data != null;
        return new Response(StatusCode.SUCCESS,"获取成功",data.getData());
    }

    @Override
    public Response deleteTask(String name) {
        //判断任务的状态，只有不在运行的可以删除
        Task task = taskMapper.selectOne(new QueryWrapper<Task>().eq("name",name));
        if(task==null){
            return new Response(StatusCode.NOT_FOUND,"该任务不存在");
        }
        if(task.getStatus()==1){
            return new Response(StatusCode.FAIL_DELETE,"任务正在运行中，不可删除");
        }

        int row = taskMapper.delete(new QueryWrapper<Task>().eq("name",name));
        if(row>0){
            //调用接口删除
            RestTemplate restTemplate = new RestTemplate();
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            Map<String,String> body = new HashMap<>();
            body.put("job_name",name);
            HttpEntity<Map> requestBody = new HttpEntity<>(body,headers);
            Response response = restTemplate.postForEntity(Constant.DEL_TASK_URL,requestBody,Response.class).getBody();
            assert response != null;
            if(response.getCode().equals("0")){
                return new Response(StatusCode.SUCCESS,"删除成功");
            }else{
                return new Response(StatusCode.FAIL_DELETE,"删除失败");
            }
        }
        return new Response(StatusCode.FAIL_DELETE,"删除失败");
    }

    @Override
    public Response getTaskList() {
        //直接调用接口
        RestTemplate restTemplate = new RestTemplate();
        Response response = restTemplate.getForEntity(Constant.GET_TASK_LIST_URL,Response.class).getBody();
        assert response != null;
        return new Response(StatusCode.SUCCESS,"获取成功",response.getData());
    }

    @Override
    public Response getTaskByName(String name) {
        //直接调用接口
        String url = Constant.GET_TASK_URL + name;
        RestTemplate restTemplate = new RestTemplate();
        Response response = restTemplate.getForEntity(url,Response.class).getBody();
        assert response != null;
        if(response.getCode().equals("0")){
            return new Response(StatusCode.SUCCESS,"获取成功",response.getData());
        }
        return new Response(StatusCode.NOT_FOUND,"获取失败");
    }

    @Override
    public Response adjustTask(Map<String, String> map) {
        RestTemplate restTemplate = new RestTemplate();
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<Map> requestBody = new HttpEntity<>(map,headers);
        Response response = restTemplate.postForEntity(Constant.ADJUST_TASK_URL,requestBody,Response.class).getBody();
        assert response != null;
        if(response.getCode().equals("0")){
            //修改数据库里task表中的resource资源使用量字段
            //val后期需要根据map里的字段进行更新
            String val = JSONObject.toJSONString(map);
            UpdateWrapper<Task> wrapper = new UpdateWrapper<>();
            wrapper.eq("name",map.get("job_name")).set("resource", val);
            int row = taskMapper.update(null, wrapper);
            if(row>0){
                return new Response(StatusCode.SUCCESS,"更新成功");
            }else{
                return new Response(StatusCode.FAIL_UPDATE,"更新失败");
            }
        }
        return new Response(StatusCode.FAIL_UPDATE,"更新失败");
    }

    @Override
    public Response getTaskByUserId(String id) {
        return null;
    }

    @Override
    public Response getUserTaskList() {
        return null;
    }

    @Override
    public Response getUserTaskByName(String name) {
        return null;
    }

    @Override
    public Response upload_train_config(MultipartFile file) {
        RestTemplate restTemplate = new RestTemplate();
        //请求头
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);
        //构建请求体
        MultiValueMap<String,Object> body = new LinkedMultiValueMap<>();
        InputStreamUtil inputStream = null;
        try {
            inputStream = new InputStreamUtil(file.getInputStream(),file.getSize(),file.getOriginalFilename());
        } catch (IOException e) {
            e.printStackTrace();
        }
        body.add("file",inputStream);
        //发送请求
        HttpEntity<MultiValueMap> requestEntity = new HttpEntity<>(body,headers);
        Response response = restTemplate.postForEntity(Constant.UPLOAD_TRAIN_CONFIG,requestEntity,Response.class).getBody();
        assert response != null;
        if(response.getCode().equals("0")){
            return new Response(StatusCode.SUCCESS,"文件上传成功");
        }else{
            return new Response(StatusCode.FAIL_UPLOAD,response.getMsg());
        }
    }

    @Override
    public Response delete_train_config(String name) {
        RestTemplate restTemplate = new RestTemplate();
        String url = Constant.DELETE_TRAIN_CONFIG + name;
        //请求头
        HttpHeaders headers = new HttpHeaders();
        //发送请求
        HttpEntity<MultiValueMap> requestEntity = new HttpEntity<>(null,headers);
        Response response = restTemplate.exchange(url, HttpMethod.DELETE, requestEntity,Response.class).getBody();
        assert response != null;
        if(response.getCode().equals("0")){
            return new Response(StatusCode.SUCCESS,"删除成功");
        }else{
            return new Response(StatusCode.FAIL_DELETE,response.getMsg());
        }
    }
}
