package com.sjtu.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.sjtu.common.Constant;
import com.sjtu.common.Response;
import com.sjtu.common.StatusCode;
import com.sjtu.entity.Image;
import com.sjtu.mapper.ImageMapper;
import com.sjtu.service.ImageService;
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
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


@Service
public class ImageServiceImpl implements ImageService {
    @Autowired
    ImageMapper imageMapper;

    IdUtil create_image_id  = new IdUtil(1,1);

    @Override
    public Response pushImage(Map<String,String> map, MultipartFile file, HttpServletRequest request) {
        String imageName = map.get("imageName");
        String imageVersion = map.get("imageVersion");
        String information = map.get("information");
        String tag = map.get("tag");

        //先插入本地数据库
        //获取token
        String token = request.getHeader("Token");
        Image image = new Image();
        image.setId(create_image_id.generateNextId());
        image.setName(imageName);
        image.setVersion(imageVersion);
        image.setTag(tag);
        image.setInformation(information);
        image.setUserId(JwtUtil.getClaim(token,"id"));

        //检查该任务的name与version是否存在于数据库
        List<Image> list = imageMapper.selectList(new QueryWrapper<Image>().eq("name",image.getName()).eq("version",image.getVersion()));
        if(list.size()!=0){
            return new Response(StatusCode.FAIL_INSERT,"该镜像名称与版本存在于数据库中，本地数据库插入失败");
        }
        //插入
        int row = imageMapper.insert(image);
        if(row>0){
            //调用接口将镜像存入镜像仓库
            RestTemplate restTemplate = new RestTemplate();
            String url = Constant.PUSH_IMAGE_URL + imageName + "&imageVersion=" + imageVersion;
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
            Response response = restTemplate.postForEntity(url,requestEntity,Response.class).getBody();
            assert response != null;
            if(response.getCode().equals("0")){
                return new Response(StatusCode.SUCCESS,"镜像上传成功");
            }else{
                return new Response(StatusCode.FAIL_UPLOAD,"镜像上传失败");
            }
        }
        return new Response(StatusCode.FAIL_UPLOAD,"镜像上传失败");
    }

    @Override
    public Response getAllImage() {
        QueryWrapper<Image> wrapper = new QueryWrapper<>();
        List<Image> data = imageMapper.selectList(wrapper);
        if(data!=null){
            return new Response(StatusCode.SUCCESS,"获取成功",data);
        }
        return new Response(StatusCode.NOT_FOUND,"获取失败");
    }

    @Override
    public Response getImageByPage(String page_now, String page_size) {
        Page<Image> page = new Page<>(Integer.parseInt(page_now),Integer.parseInt(page_size));
        QueryWrapper<Image> wrapper = new QueryWrapper<>();
        Page<Image> Image_Page = imageMapper.selectPage(page,wrapper);
        Map<String,Object> data = new HashMap<>();
        if(Image_Page!=null){
            data.put("total",Image_Page.getTotal());
            data.put("list",Image_Page.getRecords());
            return new Response(StatusCode.SUCCESS,"获取成功",data);
        }
        return new Response(StatusCode.NOT_FOUND,"获取失败");
    }

    @Override
    public Response deleteImage(String imageName,String imageVersion) {
        //先删除本地的数据库中的镜像
        QueryWrapper<Image> wrapper = new QueryWrapper<>();
        wrapper.eq("name",imageName).eq("version",imageVersion);
        int row = imageMapper.delete(wrapper);
        if(row>0){
            //调用删除接口删除镜像仓库里的镜像
            RestTemplate restTemplate = new RestTemplate();
            String url = Constant.DEL_IMAGE_URL + imageName + "&imageVersion=" + imageVersion;
            //请求头
            HttpHeaders headers = new HttpHeaders();
            //发送请求
            HttpEntity<MultiValueMap> requestEntity = new HttpEntity<>(null,headers);
            Response response = restTemplate.exchange(url, HttpMethod.DELETE, requestEntity,Response.class).getBody();
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
    public Response getImageByName(String name) {
        QueryWrapper<Image> wrapper = new QueryWrapper<>();
        wrapper.like("name",name);
        List<Image> data = imageMapper.selectList(wrapper);
        return new Response(StatusCode.SUCCESS,"查询成功",data);
    }

    @Override
    public Response pullImage(String imageName, String imageVersion,HttpServletResponse response) throws IOException {
        //调用接口下载镜像
        String url = Constant.PULL_IMAGE_URL + imageName + "&imageVersion=" + imageVersion;
        return new Response(StatusCode.SUCCESS,"下载成功",url);
    }

    @Override
    public Response getUserAllImage(HttpServletRequest request) {
        String token = request.getHeader("Token");
        QueryWrapper<Image> wrapper = new QueryWrapper<>();
        wrapper.eq("user_id",JwtUtil.getClaim(token, Constant.ID));
        List<Image> data = imageMapper.selectList(wrapper);
        if(data!=null){
            return new Response(StatusCode.SUCCESS,"获取成功",data);
        }
        return new Response(StatusCode.NOT_FOUND,"获取失败");
    }

    @Override
    public Response getUserImageByPage(String page_now, String page_size, HttpServletRequest request) {
        String token = request.getHeader("Token");
        Page<Image> page = new Page<>(Integer.parseInt(page_now),Integer.parseInt(page_size));
        QueryWrapper<Image> wrapper = new QueryWrapper<>();
        wrapper.eq("user_id",JwtUtil.getClaim(token,Constant.ID));
        Page<Image> Image_Page = imageMapper.selectPage(page,wrapper);
        Map<String,Object> data = new HashMap<>();
        if(Image_Page!=null){
            data.put("total",Image_Page.getTotal());
            data.put("list",Image_Page.getRecords());
            return new Response(StatusCode.SUCCESS,"获取成功",data);
        }
        return new Response(StatusCode.NOT_FOUND,"获取失败");
    }

    @Override
    public Response getUserImageByName(String name, HttpServletRequest request) {
        String token = request.getHeader("Token");
        QueryWrapper<Image> wrapper = new QueryWrapper<>();
        wrapper.like("name",name).eq("user_id",JwtUtil.getClaim(token,Constant.ID));
        List<Image> data = imageMapper.selectList(wrapper);
        return new Response(StatusCode.SUCCESS,"查询成功",data);
    }
}
