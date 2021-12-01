package com.sjtu.service;

import com.sjtu.common.Response;
import org.springframework.web.multipart.MultipartFile;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.Map;

public interface ImageService {
    /*插入镜像*/
    Response pushImage(Map<String,String> map, MultipartFile file, HttpServletRequest request) throws IOException;
    /*获取所有的镜像*/
    Response getAllImage();
    /*分页查询*/
    Response getImageByPage(String page_now,String page_size);
    /*删除镜像*/
    Response deleteImage(String imageName,String imageVersion);
    /*根据名称搜索镜像*/
    Response getImageByName(String name);
    /*下载镜像*/
    Response pullImage(String imageName, String imageVersion, HttpServletResponse response) throws IOException;

    /*获取用户的全部镜像*/
    Response getUserAllImage(HttpServletRequest request);
    /*用户分页查询*/
    Response getUserImageByPage(String page_now,String page_size, HttpServletRequest request);
    /*用户根据名称获取镜像*/
    Response getUserImageByName(String name, HttpServletRequest request);
}
