package com.sjtu.common;

import java.util.LinkedHashMap;
import java.util.Map;

/*常量*/
public class Constant {
    public Constant() {
    }

    /** 设置redis过期时间: 60分钟 */
    public static final long REFRESH_EXPIRE_TIME = 60 * 60 * 1000;

    /*设置access_token过期时间：30分钟*/
    public static final long ACCESS_EXPIRE_TIME = 30 * 60 * 1000;

    //token并发问题 10s过渡时间
    public static final long REFRESH_TRANSITION_EXPIRE_TIME = 10 * 1000;

    //redis-key-前缀-shiro:refresh_token:
    public static final String PREFIX_SHIRO_REFRESH_TOKEN = "shiro:refresh_token:";

    //redis-key-前缀-shiro:refresh_token:transition:
    public static final String PREFIX_SHIRO_REFRESH_TOKEN_TRANSITION = "shiro:refresh_token_transition:";

    //JWT-id
    public static final String ID = "id";

    //JWT-currentTimeMillis:
    public static final String CURRENT_TIME_MILLIS = "currentTimeMillis";

    //修改密码次数上限
    public static final int RESET_PASSWORD_LIMIT_TIME = 5;

    //设置邮箱验证 链接失效时间
    public static final long LINK_EXPIRE_TIME = 2*60*1000;

    //普通用户初始权限
    public static final Map<String,Boolean> USER_AUTHORITY = new LinkedHashMap<String,Boolean>();
    static{
        USER_AUTHORITY.put("user:pullImage",true);
        USER_AUTHORITY.put("user:pushImage",true);
        USER_AUTHORITY.put("user:deleteTask",true);
        USER_AUTHORITY.put("user:submitTask",true);
        USER_AUTHORITY.put("user:deleteImage",true);
        USER_AUTHORITY.put("user:getUserAllImage",true);
        USER_AUTHORITY.put("user:getUserTaskList",true);
        USER_AUTHORITY.put("user:getUserTaskByName",true);
        USER_AUTHORITY.put("user:getTrainConfigList",true);
        USER_AUTHORITY.put("user:getUserImageByName",true);
        USER_AUTHORITY.put("user:getUserImageByPage",true);
        USER_AUTHORITY.put("user:Pod_monitor",true);
        USER_AUTHORITY.put("user:uploadTrainConfig",true);
        USER_AUTHORITY.put("user:deleteTrainConfig",true);
    }

    //管理员初始权限
    public static final Map<String,Boolean> ADMIN_AUTHORITY = new LinkedHashMap<>();
    static {
        ADMIN_AUTHORITY.put("admin:pullImage",true);
        ADMIN_AUTHORITY.put("admin:pushImage",true);
        ADMIN_AUTHORITY.put("admin:deleteTask",true);
        ADMIN_AUTHORITY.put("admin:submitTask",true);
        ADMIN_AUTHORITY.put("admin:deleteImage",true);
        ADMIN_AUTHORITY.put("admin:getAllImage",true);
        ADMIN_AUTHORITY.put("admin:getTaskList",true);
        ADMIN_AUTHORITY.put("admin:getTaskByName",true);
        ADMIN_AUTHORITY.put("admin:getImageByName",true);
        ADMIN_AUTHORITY.put("admin:getImageByPage",true);
        ADMIN_AUTHORITY.put("admin:getTrainConfigList",true);
        ADMIN_AUTHORITY.put("admin:Total_Monitor",true);
        ADMIN_AUTHORITY.put("admin:Pod_Monitor",true);
        ADMIN_AUTHORITY.put("admin:ifMonitorNode",true);
        ADMIN_AUTHORITY.put("admin:endMonitorNode",true);
        ADMIN_AUTHORITY.put("admin:startMonitorNode",true);
        ADMIN_AUTHORITY.put("admin:uploadTrainConfig",true);
        ADMIN_AUTHORITY.put("admin:deleteTrainConfig",true);
    }


    //监控外部接口
    public static final String TOTAL_MONITOR_URL = "http://172.16.20.190:3000/d/6Y1mV247k/k8s-zheng-ti-jian-kong?orgId=1&refresh=30s";
    public static final String POD_MONITOR_URL = "http://172.16.20.190:3000/d/dAh43sVnk/k8s-podjian-kong?orgId=1&var-CPU_NAME=EXPC";
    public static final String IF_MONITOR_URL = "http://172.16.20.190:15000/monitor/ifMonitorNode";
    public static final String END_MONITOR_URL = "http://172.16.20.190:15000/monitor/endMonitorNode";
    public static final String START_MONITOR_URL = "http://172.16.20.190:15000/monitor/endMonitorNode";

    //镜像外部接口
    public static final String PUSH_IMAGE_URL = "http://172.16.20.190:15000/image/pushImage?imageName=";
    public static final String DEL_IMAGE_URL = "http://172.16.20.190:15000/image/deleteImage?imageName=";
    public static final String  PULL_IMAGE_URL = "http://172.16.20.190:15000/image/pullImage?imageName=";

    //任务外部接口
    public static final String SUBMIT_TASK_URL = "http://172.16.20.190:15000/task/submit";
    public static final String GET_CONFIG_URL = "http://172.16.20.190:15000/task/getTrainConfigList";
    public static final String DEL_TASK_URL = "http://172.16.20.190:15000/task/delete";
    public static final String GET_TASK_LIST_URL = "http://172.16.20.190:15000/task/getTaskList";
    public static final String GET_TASK_URL = "http://172.16.20.190:15000/task/selectOne?job_name=";
    public static final String ADJUST_TASK_URL = "http://172.16.20.190:15000/task/adjust";
    public static final String UPLOAD_TRAIN_CONFIG = "http://172.16.20.190:15000/task/upload_train_config";
    public static final String DELETE_TRAIN_CONFIG = "http://172.16.20.190:15000/task/delete_train_config?config_file_name=";

}
