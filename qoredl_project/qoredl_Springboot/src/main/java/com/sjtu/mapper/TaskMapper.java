package com.sjtu.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.sjtu.entity.Task;
import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;

@Mapper
@Repository
public interface TaskMapper extends BaseMapper<Task> {
}
