package com.sjtu.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.sjtu.entity.ResetPassword;
import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;

@Mapper
@Repository
public interface ResetPasswordMapper extends BaseMapper<ResetPassword> {
}
