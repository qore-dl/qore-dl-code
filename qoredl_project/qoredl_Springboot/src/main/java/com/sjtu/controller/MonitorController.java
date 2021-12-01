package com.sjtu.controller;

import com.sjtu.common.Constant;
import com.sjtu.common.Response;
import com.sjtu.common.StatusCode;
import org.apache.shiro.authz.annotation.Logical;
import org.apache.shiro.authz.annotation.RequiresPermissions;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

/*实现监控*/
@RestController
public class MonitorController {
    @GetMapping("/Total_Monitor")
    @RequiresPermissions(value = {"admin:Total_Monitor"})
    public Response Total_Monitor(){
        return new Response(StatusCode.SUCCESS,"获取成功", Constant.TOTAL_MONITOR_URL);
    }

    @PostMapping("/Pod_Monitor")
    @RequiresPermissions(value = {"admin:Pod_Monitor","user:Pod_Monitor"}, logical = Logical.OR)
    public Response Pod_Monitor(@RequestBody Map<String,String> map){
        String job_name = map.get("job_name");
        //分割字符串
        String task_id = job_name.substring(4);
        String url = Constant.POD_MONITOR_URL + task_id + "&var-GPU_NAME=EXPG" + task_id + "&refresh=5s";
        return new Response(StatusCode.SUCCESS,"获取成功", url);
    }

    @GetMapping("/ifMonitorNode")
    @RequiresPermissions(value = {"admin:ifMonitorNode"})
    public Response ifMonitorNode(){
        RestTemplate restTemplate = new RestTemplate();
        Response response = restTemplate.getForEntity(Constant.IF_MONITOR_URL,Response.class).getBody();
        return new Response(StatusCode.SUCCESS,"请求成功",response.getData());
    }

    @GetMapping("/endMonitorNode")
    @RequiresPermissions(value = {"admin:endMonitorNode"})
    public Response endMonitorNode(){
        RestTemplate restTemplate = new RestTemplate();
        Response response = restTemplate.getForEntity(Constant.END_MONITOR_URL,Response.class).getBody();
        return new Response(StatusCode.SUCCESS,"暂停成功",response.getData());
    }

    @GetMapping("/startMonitorNode")
    @RequiresPermissions(value = {"admin:startMonitorNode"})
    public Response startMonitorNode(){
        RestTemplate restTemplate = new RestTemplate();
        Response response = restTemplate.getForEntity(Constant.START_MONITOR_URL,Response.class).getBody();
        return new Response(StatusCode.SUCCESS,"启动成功",response.getData());
    }


}
