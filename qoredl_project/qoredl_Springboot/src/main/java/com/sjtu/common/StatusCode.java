package com.sjtu.common;

/*状态码*/
public class StatusCode {
    //成功
    public static final String SUCCESS = "200";
    //登录失败
    public static final String FAIL_LOGIN = "400";
    //注册失败
    public static final String FAIL_REGISTER = "401";
    //账户激活失败
    public static final String FAIL_ACTIVATE = "402";
    //登录过期
    public static final String TOKEN_EXPIRED = "403";
    //空指针错误
    public static final String NULL_POINTER = "405";
    //请求参数未给全
    public static final String PARAM_NOT_READY = "406";
    //重置密码失败
    public static final String FAIL_RESET_PWD = "407";
    //插入数据库失败
    public static final String FAIL_INSERT = "408";
    //删除失败
    public static final String FAIL_DELETE = "409";
    //任务提交失败
    public static final String FAIL_SUBMIT = "410";
    //权限问题
    public static final String NO_AUTHORITY = "411";
    //远程接口连接失败
    public static final String FAIL_CONNECT = "412";
    //更新数据库失败
    public static final String FAIL_UPDATE = "413";
    //未找到
    public static final String NOT_FOUND = "500";
    //上传失败
    public static final String FAIL_UPLOAD = "501";
}
