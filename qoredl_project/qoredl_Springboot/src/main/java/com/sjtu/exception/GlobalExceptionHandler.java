package com.sjtu.exception;

import com.auth0.jwt.exceptions.TokenExpiredException;
import com.sjtu.common.Response;
import com.sjtu.common.StatusCode;
import org.apache.shiro.authc.AuthenticationException;
import org.apache.shiro.authc.IncorrectCredentialsException;
import org.apache.shiro.authz.AuthorizationException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.client.RestClientException;
import org.springframework.web.servlet.NoHandlerFoundException;

import javax.servlet.http.HttpServletRequest;
import java.io.IOException;

@ControllerAdvice
public class GlobalExceptionHandler {
    private static final Logger logger = LoggerFactory.getLogger(GlobalExceptionHandler.class);
    /*处理自定义的异常*/
    @ResponseBody
    @ExceptionHandler(value = ServiceException.class)
    public Response serviceExceptionHandler(HttpServletRequest request, ServiceException e){
        logger.error("业务异常，code:" + e.getCode() + "  msg:" + e.getMsg());
        return new Response(e.getCode(),e.getMsg());
    }

    /*处理登录认证的异常*/
    @ResponseBody
    @ExceptionHandler(value = {AuthenticationException.class, IncorrectCredentialsException.class})
    public Response authenticationExceptionHandler(HttpServletRequest request, AuthenticationException e){
        logger.error("登录失败，msg: " + e.getMessage());
        return new Response(StatusCode.FAIL_LOGIN,"用户名或密码错误");
    }

    @ResponseBody
    @ExceptionHandler(value = AuthorizationException.class)
    public Response AuthorizationExceptionHandler(HttpServletRequest request, AuthorizationException e){
        logger.error("无权限访问，msg: " + e.getMessage());
        return new Response(StatusCode.NO_AUTHORITY,"无权限访问");
    }

    /*处理请求缺少参数异常*/
    @ResponseBody
    @ExceptionHandler(value = HttpMessageNotReadableException.class)
    public Response httpMessageNotReadableExceptionHandler(HttpServletRequest request, HttpMessageNotReadableException e){
        logger.error("请求参数不全，msg: " + e.getMessage());
        return new Response(StatusCode.PARAM_NOT_READY,"请求参数不全");
    }

    /*处理访问flask等其他接口时的异常错误*/
    @ResponseBody
    @ExceptionHandler(value = RestClientException.class)
    public Response RestClientExceptionHandler(HttpServletRequest request, RestClientException e){
        logger.error("远程接口异常，msg: " + e.getMessage());
        return new Response(StatusCode.FAIL_CONNECT,"远程接口连接失败");
    }

    /*处理空指针异常*/
    @ResponseBody
    @ExceptionHandler(value = NullPointerException.class)
    public Response nullPointerExceptionHandler(HttpServletRequest request, NullPointerException e){
        logger.error("空指针异常，msg: " + e.getMessage());
        return new Response(StatusCode.NULL_POINTER,"空指针异常");
    }

    /*处理token过期*/
    @ResponseBody
    @ExceptionHandler(value = TokenExpiredException.class)
    public void TokenExpiredExceptionHandler(HttpServletRequest request, TokenExpiredException e){
        logger.error("Token expired or incorrect");
    }

    /*处理IO异常*/
    @ResponseBody
    @ExceptionHandler(value = IOException.class)
    public void IOExceptionHandler(HttpServletRequest request,IOException e){
        logger.error("文件输入流转换错误");
    }

    /*处理NoHandlerFoundException异常*/
    @ResponseBody
    @ExceptionHandler(value = NoHandlerFoundException.class)
    public Response exceptionHandler(HttpServletRequest request, NoHandlerFoundException e){
        logger.error("服务错误:" + e.getMessage());
        return new Response(StatusCode.NOT_FOUND,"服务错误");
    }
}
