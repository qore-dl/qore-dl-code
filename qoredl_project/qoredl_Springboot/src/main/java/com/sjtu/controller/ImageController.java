package com.sjtu.controller;

import com.sjtu.common.Response;
import com.sjtu.service.ImageService;
import org.apache.shiro.authz.annotation.Logical;
import org.apache.shiro.authz.annotation.RequiresPermissions;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.Map;

@RestController
public class ImageController {
    @Autowired
    ImageService imageService;

    @PostMapping("/pushImage")
    @RequiresPermissions(value = {"user:pushImage","admin:pushImage"},logical = Logical.OR)
    public Response pushImage(@RequestParam Map<String,String> map, @RequestParam("file") MultipartFile file, HttpServletRequest request) throws IOException {
        return imageService.pushImage(map, file, request);
    }

    @PostMapping("/deleteImage")
    @RequiresPermissions(value = {"user:deleteImage","admin:deleteImage"},logical = Logical.OR)
    public Response deleteImage(@RequestBody Map<String,String> map){
        return imageService.deleteImage(map.get("imageName"),map.get("imageVersion"));
    }

    @PostMapping("/pullImage")
    @RequiresPermissions(value = {"user:pullImage","admin:pullImage"},logical = Logical.OR)
    public Response pullImage(@RequestBody Map<String,String> map, HttpServletResponse response) throws IOException {
        return imageService.pullImage(map.get("imageName"),map.get("imageVersion"), response);
    }

    @PostMapping("/getAllImage")
    @RequiresPermissions(value = {"admin:getAllImage"})
    public Response getAllImage(){
        return imageService.getAllImage();
    }

    @PostMapping("/getImageByPage")
    @RequiresPermissions(value = {"admin:getImageByPage"})
    public Response getImageByPage(@RequestBody Map<String,String> map){
        return imageService.getImageByPage(map.get("page_now"),map.get("page_size"));
    }

    @PostMapping("/getImageByName")
    @RequiresPermissions(value = {"admin:getImageByName"})
    public Response getImageByName(@RequestBody Map<String,String> map){
        return imageService.getImageByName(map.get("name"));
    }

    @PostMapping("/getUserAllImage")
    @RequiresPermissions(value = {"user:getUserAllImage"})
    public Response getUserAllImage(HttpServletRequest request){
        return imageService.getUserAllImage(request);
    }

    @PostMapping("/getUserImageByPage")
    @RequiresPermissions(value = {"user:getUserImageByPage"})
    public Response getUserImageByPage(@RequestBody Map<String,String> map, HttpServletRequest request){
        return imageService.getUserImageByPage(map.get("page_now"),map.get("page_size"),request);
    }

    @PostMapping("/getUserImageByName")
    @RequiresPermissions(value = {"user:getUserImageByName"})
    public Response getUserImageByName(@RequestBody Map<String,String> map, HttpServletRequest request){
        return imageService.getUserImageByName(map.get("name"),request);
    }
}
