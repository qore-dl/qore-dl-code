<template>
  <div style="padding: 32px">

    <div style="
    height: 200px;
    display: flex;
    justify-content: space-between;
      ">
      <div style="flex: 1">
        <div style="
          color: rgb(32, 33, 36);
          font-size: 36px;
          line-height: 44px;
          font-weight: bold;
          font-family: zeitung, sans-serif;">
          任务管理
        </div>

        <div style="
            margin-top: 20px;
            color:	#808080;
            font-size: 14px;
            font-weight: 400;
            line-height: 22px;
            max-width: 485px;
        ">
          <span>在这里管理您的任务。</span><br/>
          任务管理支持对任务的创建与管理，同时支持对镜像任务训练的启动、暂停、停止，以及查看任务日志等。
        </div>

<!--
        <el-button style="background-color: #333333;color: #FFFFFF;margin-top: 20px;" round @click="$router.push('/uploadtask')">+ 创建任务</el-button>
        <el-button @click="load">按钮</el-button>
-->

      </div>


      <div style="text-align: center;width: 200px;">

        <svg class="icon" aria-hidden="true" style="font-size: 200px">
          <use xlink:href="#icon-moxingxunlian"></use>
        </svg>

      </div>

    </div>

    <el-card style="height: 100px; margin-bottom: 10px" v-for="item in tableData">

      <div style="display: flex">
        <div style="width: 100px;height: 60px">
          <svg class="icon" aria-hidden="true" style="font-size:60px">
            <use xlink:href="#icon-ARIMA"></use>
          </svg>
        </div>

        <div style="width: 20%">
          <div style="font-weight: bold;font-size: 20px">{{item.name}}</div>
          <div style="margin-top:10px;font-size: 12px;color: #5D5D5D">{{item.information}}</div>
        </div>

        <div style="flex: 1; display: flex;align-items: center;">

          <div style="display: flex;">


            <div style="color: #545454"><svg class="icon" aria-hidden="true">
              <use xlink:href="#icon-jindu"></use>
            </svg>状态:</div>

            <div style="width: 150px">{{item.status}}</div>

            <div style="color: #545454;cursor:pointer;">
              <el-tooltip class="item" effect="dark" content="具体信息" placement="top">
              <svg class="icon" aria-hidden="true" font-size="25px" @click="viewDetail(item.name)">
                <use xlink:href="#icon-chakan3"></use>
              </svg>
              </el-tooltip>
            </div>

            <div style="width: 50px"></div>

            <div style="color: #545454;cursor:pointer;">
              <el-tooltip class="item" effect="dark" content="查看资源" placement="top">
                <svg class="icon" aria-hidden="true" font-size="25px" @click="viewResource(item.name)">
                  <use xlink:href="#icon-chakan2"></use>
                </svg>
              </el-tooltip>
            </div>

            <div style="width: 50px"></div>

            <div style="color: #545454;cursor:pointer;">
              <el-tooltip class="item" effect="dark" content="调整资源" placement="top">
              <svg class="icon" aria-hidden="true" font-size="22px" @click="changeResource(item.name)">
                <use xlink:href="#icon-tiaozheng"></use>
              </svg>
              </el-tooltip>
              </div>

          </div>

        </div>


<!--        <div style="width: 100px;margin:auto;"><el-button type="info" @click="use(item.id)" round >开始</el-button></div>
        <div style="width: 100px;margin:auto;"><el-button type="info" @click="use(item.id)" round >暂停</el-button></div>-->
        <div style="width: 100px;margin:auto;"><el-button type="info" @click="deleteTask(item.name)" round >删除</el-button></div>

      </div>


    </el-card>

    <el-empty v-if="isEmpty" :image-size="200"></el-empty>

    <el-dialog
        title="调整资源"
        :visible.sync="changeResourceDialogVisible"
        width="30%"
        :before-close="handleClose"
        >

      <div style="color: dimgray;margin-bottom: 10px">cpu_allocate 占据CPU数量,-1不做限制,单位为m (1 logcial CPU = 1000m)</div>
      <div style="margin-bottom: 10px"><el-input-number :controls="false" style="width: 200px;" v-model="changeResourceForm.cpu_allocate" placeholder="-1"></el-input-number> </div>

      <div style="color: dimgray;margin-bottom: 10px">mem_allocate 分配内存数量,-1不做限制,单位为MB</div>
      <div style="margin-bottom: 10px"><el-input-number :controls="false" style="width: 200px;" v-model="changeResourceForm.mem_allocate" placeholder="-1"></el-input-number> </div>

      <div style="color: dimgray;margin-bottom: 10px">backend 分布式训练主节点数量</div>
      <div style="margin-bottom: 10px"><el-input-number :controls="false" style="width: 200px;" v-model="changeResourceForm.master_replicas" placeholder="1"></el-input-number> </div>

      <div style="color: dimgray;margin-bottom: 10px">num_workers 分布式训练从节点数量</div>
      <div style="margin-bottom: 10px"><el-input-number :controls="false" style="width: 200px;" v-model="changeResourceForm.worker_replicas" placeholder="1"></el-input-number> </div>


      <span slot="footer" class="dialog-footer">
      <el-button type="primary" @click="changeResourceConfirm">确 定</el-button>
      </span>


    </el-dialog>

    <el-dialog
        title="具体信息"
        :visible.sync="detailDialogVisible"
        width="30%"
        :before-close="handleClose"
    >
      <div v-for="item in taskDetail" style="width: 100%">
        <div style="display: flex;justify-content: space-between">
          <div style="width: 50%">{{item.name}}</div>
          <div style="width: 50%">{{item.value}}</div>
        </div>

        <el-divider></el-divider>

      </div>


    </el-dialog>


  </div>
</template>

<script>

import axios from 'axios'
import request from "../utils/request";

export default {
  name: "ImageManage",
  data(){
    return{
      input:'',
      tableData:[
      ],
      isEmpty:true,
      changeResourceForm:{
        job_name:"",
        cpu_allocate: 2000,
        mem_allocate: 2000,
        master_replicas: 1,
        worker_replicas: 1
      },

      changeResourceDialogVisible:false,
      detailDialogVisible:false,
      taskDetail:[],
    }


  },
  created() {
    this.load();
  },
  methods:{
    //初始化
    load(){
      console.log("load");
      request.get("api/getTaskList").then(res=>{
          if(res.code=='200'){

            this.tableData=[];
            let running=res.data.running;
            for(let key in running){
              let item={};
              item['name']=key;
              item['status']='running';
              this.tableData.push(item);
            }

            let scheduling=res.data.scheduling;
            for(let key in scheduling){
              let item={};
              item['name']=key;
              item['status']='scheduling';
              this.tableData.push(item);
            }

            /*let adjusting=res.data.adjusting;
            for(let key in adjusting){
              let item={};
              item['name']=key;
              item['status']='adjusting';
              this.tableData.push(item);
            }*/


          }else{
            this.$message({ type:"error", message:"调用接口失败" });
            this.isEmpty=true;
          }

          if(this.tableData===[]){
            //console.log('is empty');
            this.isEmpty=true;
          }else{
            this.isEmpty=false;
          }

      })
    },

    //删除任务
    deleteTask(name){

      request.post("api/deleteTask",{job_name:name}).then(res=>{
        if(res.code=='200'){
          this.$message({ type:"success", message:"删除任务成功" });
          this.load();
        }else{
          this.$message({ type:"error", message:"删除任务失败" });
        }

      })
    },

    //更改资源
    changeResource(name){
      console.log("change");
      this.changeResourceDialogVisible=true;
      this.changeResourceForm.job_name=name;
    },
    changeResourceConfirm(){

      request.post("api/adjustTask",this.changeResourceForm).then(res=>{
        if(res.code=='200'){
          this.$message({ type:"success", message:"调整成功" });
          this.changeResourceDialogVisible = false;
        }else{
          this.$message({ type:"error", message:"调整失败" });
        }

      })



    },

    //查看具体信息
    viewDetail(name){
      request.post("api/getTaskByName",{ job_name:name}).then(res=>{
        if(res.code=='200'){
          this.taskDetail=[];
          for(let key in res.data){
            let item={};
            item['name']=key;
            item['value']=res.data[key];
            this.taskDetail.push(item);
          }
          this.detailDialogVisible=true;

        }else{
          this.$message({ type:"error", message:"删除任务失败" });
        }

      })
    },

    /*查看资源*/
    viewResource(name){

      request.post("api/Pod_Monitor",{ job_name:name}).then(res=>{
        if(res.code=='200'){

          console.log(res.data);
          let urlStr=res.data;
          sessionStorage['urlStr'] = urlStr;
          this.$router.push('/taskmonitor');
        }else{
          this.$message({ type:"error", message:"访问资源失败" });
        }
      })

    },

    test(name){

    },

    handleClose(done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done();
        })
        .catch(_ => {});
    }

  },


}
</script>

<style >

.el-input-number .el-input__inner {
  text-align: left !important;
}

.el-divider--horizontal{
  margin: 8px 0;
  background: 0 0;
  border-top: 3px dashed #e8eaec;
}
</style>