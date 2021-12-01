<template>
  <div style="padding: 32px">

    <div style="width: 800px;margin: 0 auto;">

      <div style="display: flex;justify-content: space-between">
        <div style="font-weight: bold;font-size: 25px"><svg class="icon" aria-hidden="true">
          <use xlink:href="#icon-shiyong"></use>
        </svg> 训练任务</div>

<!--        <div>
          <el-button @click="back">上一步</el-button>
          <el-button @click="next">下一步</el-button>
        </div>-->

      </div>


      <el-divider></el-divider>

<!--      <el-steps :active="active" finish-status="wait" align-center>

        <el-step title="步骤 1" ></el-step>
        <el-step title="步骤 2" ></el-step>
        <el-step title="步骤 3" ></el-step>

      </el-steps>-->


      <el-card style="margin-top: 20px">
        <div v-show="active==0">

          <div style="padding: 20px;color: #5D5D5D;height: 100%;position: relative">
            <div style="margin-bottom: 15px">
              <svg class="icon" aria-hidden="true" style="font-size: 20px">
                <use xlink:href="#icon-a-Calendar2"></use>
              </svg>
              任务名称</div>
            <el-input style="margin-bottom: 20px" v-model="form.name" placeholder="请输入" ></el-input>

            <div style="margin-bottom: 15px">
              <svg class="icon" aria-hidden="true" style="font-size: 20px">
                <use xlink:href="#icon-a-Calendar2"></use>
              </svg>
              任务描述</div>
            <el-input style="margin-bottom: 20px" v-model="form.name" placeholder="不超过20字" ></el-input>

          </div>


        </div>

        <div v-show="active==1">
          <div style="text-align: center">
            <el-button @click="uploadTask">提交训练</el-button>
          </div>

          <div style="padding: 20px;color: #5D5D5D;height: 100%;position: relative">



            <div style="color: dimgray;margin-bottom: 10px">priority </div>
            <div style="display: flex">
              <div style="margin-bottom: 10px"><el-input-number :controls="false" style="width: 200px;" v-model="form.priority" placeholder="0"></el-input-number> </div>
              <div style="color: dimgray;flex: 1;height: 40px;line-height: 40px;margin-left: 10px"> 调度优先级(越大优先级越高)</div>
            </div>



            <div style="color: dimgray;margin-bottom: 10px">image_name </div>
            <div style="display: flex">
              <div style="margin-bottom: 10px"><el-input :controls="false" style="width: 200px;" v-model="form.image_name" disabled></el-input> </div>
              <div style="color: dimgray;flex: 1;height: 40px;line-height: 40px;margin-left: 10px">运行镜像</div>
            </div>


              <div style="color: dimgray;margin-bottom: 10px">training_config_file<span style="color: red"> 必选</span></div>
              <div style="display: flex">
                <div style="margin-bottom: 10px">
                  <el-select v-model="form.training_config_file" placeholder="请选择">
                    <el-option
                        v-for="item in training_config_file_options"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                    </el-option>
                  </el-select>
                </div>
                <div style="color: dimgray;flex: 1;height: 40px;line-height: 40px;margin-left: 10px">模型配置yaml文件</div>
              </div>


            <div style="color: dimgray;margin-bottom: 10px">master_replicas</div>
            <div style="display: flex">
                <div style="margin-bottom: 10px"><el-input-number :controls="false" style="width: 200px;" v-model="form.master_replicas" placeholder="1"></el-input-number> </div>
              <div style="color: dimgray;flex: 1;height: 40px;line-height: 40px;margin-left: 10px"> 分布式训练主节点数量，推荐值为1</div>
            </div>


              <div style="color: dimgray;margin-bottom: 10px">worker_replicas</div>
              <div style="display: flex">
                <div style="margin-bottom: 10px"><el-input-number :controls="false" style="width: 200px;" v-model="form.worker_replicas" placeholder="1"></el-input-number> </div>
                <div style="color: dimgray;flex: 1;height: 40px;line-height: 40px;margin-left: 10px"> 分布式训练从节点数量</div>
              </div>


                <div style="color: dimgray;margin-bottom: 10px">cpu_allocate</div>
              <div style="display: flex">
                <div style="margin-bottom: 10px"><el-input-number :controls="false" style="width: 200px;" v-model="form.cpu_allocate" placeholder="-1"></el-input-number> </div>
                <div style="color: dimgray;flex: 1;height: 40px;line-height: 40px;margin-left: 10px"> 占据CPU数量，-1不做限制，单位为m(1 logcial CPU = 1000m)</div>
              </div>



            <div style="color: dimgray;margin-bottom: 10px">mem_allocate</div>
            <div style="display: flex">

            <div style="margin-bottom: 10px"><el-input-number :controls="false" style="width: 200px;" v-model="form.mem_allocate" placeholder="-1"></el-input-number> </div>
              <div style="color: dimgray;flex: 1;height: 40px;line-height: 40px;margin-left: 10px"> 分配内存数量，-1不做限制，单位为MB</div>
            </div>


            <div style="color: dimgray;margin-bottom: 10px">backend </div>
            <div style="display: flex">

            <div style="margin-bottom: 10px">
              <el-select v-model="form.backend"  placeholder="nccl">
                <el-option label="nccl" value="nccl"></el-option>
                <el-option label="gloo" value="gloo"></el-option>
              </el-select>
            </div>

              <div style="color: dimgray;flex: 1;height: 40px;line-height: 40px;margin-left: 10px">分布式训练通信框架</div>

            </div>


                <div style="color: dimgray;margin-bottom: 10px">num_workers</div>
            <div style="display: flex">

            <div style="margin-bottom: 10px"><el-input-number :controls="false" style="width: 200px;" v-model="form.num_workers" placeholder="2"></el-input-number> </div>
              <div style="color: dimgray;flex: 1;height: 40px;line-height: 40px;margin-left: 10px"> 每节点加载数据集线程数量</div>
            </div>


                <div style="color: dimgray;margin-bottom: 10px">gpu_monitor_interval</div>
            <div style="display: flex">

            <div style="margin-bottom: 10px"><el-input-number :controls="false" style="width: 200px;" v-model="form.gpu_monitor_interval" placeholder="30"></el-input-number> </div>
              <div style="color: dimgray;flex: 1;height: 40px;line-height: 40px;margin-left: 10px"> 每节点GPU监控采样间隔,单位为s</div>
            </div>


                <div style="color: dimgray;margin-bottom: 10px">gpu_monitor_failure</div>
            <div style="display: flex">

            <div style="margin-bottom: 10px"><el-input-number :controls="false" style="width: 200px;" v-model="form.gpu_monitor_failure" placeholder="15"></el-input-number> </div>
              <div style="color: dimgray;flex: 1;height: 40px;line-height: 40px;margin-left: 10px"> GPU监控重试次数，超过则认为监控失败</div>
            </div>


                  <div style="color: dimgray;margin-bottom: 10px">pin_memory</div>
            <div style="display: flex">

            <div style="margin-bottom: 10px">
                    <el-select v-model="form.pin_memory"  placeholder="true">
                      <el-option label="true" value="true"></el-option>
                      <el-option label="false" value="false"></el-option>
                    </el-select>
                  </div>
              <div style="color: dimgray;flex: 1;height: 40px;line-height: 40px;margin-left: 10px"> 每节点加载数据集是否启用pin_memory</div>
            </div>


                  <div style="color: dimgray;margin-bottom: 10px">template_name</div>
            <div style="display: flex">

            <div style="margin-bottom: 10px"><el-input  style="width: 200px;" v-model="form.template_name" placeholder="exp"></el-input> </div>
              <div style="color: dimgray;flex: 1;height: 40px;line-height: 40px;margin-left: 10px"> 任务名</div>
            </div>


            <div style="color: dimgray;margin-bottom: 10px">task_id </div>
            <div style="display: flex">

            <div style="margin-bottom: 10px"><el-input-number :controls="false" style="width: 200px;" v-model="form.task_id"></el-input-number> </div>
              <div style="color: dimgray;flex: 1;height: 40px;line-height: 40px;margin-left: 10px">任务id，可指定，或后台全局唯一赋值</div>
            </div>


                <div style="color: dimgray;margin-bottom: 10px">retry</div>
            <div style="display: flex">

            <div style="margin-bottom: 10px"><el-input-number :controls="false" style="width: 200px;" v-model="form.retry" placeholder="0"></el-input-number> </div>
              <div style="color: dimgray;flex: 1;height: 40px;line-height: 40px;margin-left: 10px"> 任务重试，即运行之前的job时可进行备注</div>
            </div>


                <div style="color: dimgray;margin-bottom: 10px">status</div>
            <div style="display: flex">

            <div style="margin-bottom: 10px"><el-input  style="width: 200px;" v-model="form.status" placeholder="initial"></el-input> </div>
              <div style="color: dimgray;flex: 1;height: 40px;line-height: 40px;margin-left: 10px;font-size: 10px"> 任务状态，初始默认为initial,后续会变为scheduling,running, finished，failed，error等</div>
            </div>


              <div style="color: dimgray;margin-bottom: 10px">任务信息</div>

              <div><el-input v-model="information" style="width:80%"></el-input></div>


          </div>

        </div>

        <div v-show="active==2">

        </div>
      </el-card>

    </div>

  </div>
</template>

<script>

import axios from 'axios'
import request from "../utils/request";

export default {
  name: "UploadImage",
  data() {
    return {

      active: 1,
      form:{
        image_name:'',
      },
      input:undefined,
      information:'',
      training_config_file_options: [{
        value: '选项1',
        label: '黄金糕'
      }]

    };
  },
  created() {
    this.load();
  },
  methods:{
    load(){
      let name=sessionStorage['name'];
      let version=sessionStorage['version'];
      this.form.image_name='172.16.20.190:5000/'+name+":"+version;

      this.training_config_file_options=[];

      request.get("api/getTrainConfigList").then(res=>{
        if(res.code=='200'){
          this.tableData=[];
          for(let i=0;i<res.data.length;i++){
            let str=res.data[i];
            let item={};
            item['label']=str;
            item['value']=str;
            this.training_config_file_options.push(item);
          }
        }
      })



    },
    next() {
      if (this.active++ >= 2) this.active = 0;
      console.log(this.active);
    },
    back() {
      if (this.active-- <= 0) this.active = 2;
      console.log(this.active);
    },

    uploadTask(){

      if(this.form["pin_memory"]=="true"||this.form["pin_memory"]==""||this.form["pin_memory"]==undefined||this.form["pin_memory"]==null){
        this.form["pin_memory"]=1;
      }else{
        this.form["pin_memory"]=-1;
      }

      for(let key in this.form){
        if(this.form[key]==""||this.form[key]==undefined||this.form[key]==null){
          delete this.form[key];
        }
      }


      let sendObj={};
      sendObj.information=this.information;
      sendObj.data=this.form;
      sendObj.resource={};
      sendObj.resource["cpu_allocate"]=this.form["cpu_allocate"];
      sendObj.resource["mem_allocate"]=this.form["mem_allocate"];
      sendObj.resource["master_replicas"]=this.form["master_replicas"];
      sendObj.resource["worker_replicas"]=this.form["worker_replicas"];

      request.post("api/submitTask",sendObj).then(res=>{
        if(res.code=='200'){
          this.$message({ type:"success", message:"提交训练成功" });
          this.$router.push('/imagemanage');
        }else{
          this.$message({ type:"error", message:"提交训练失败" });
        }
      })

    }
  }
}
</script>

<style >
.el-input-number .el-input__inner {
  text-align: left !important;
}
</style>