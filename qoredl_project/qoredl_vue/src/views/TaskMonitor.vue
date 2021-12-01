<template>
  <div style="background-color: #111217">

    <div style="width: 70px;height: 100vh;position: fixed;left: 0;top:50px;background-color: #111217">
<!--      <div style="color:#FFFFFF;">启动监控</div>-->

      <div v-if="isRun==false" class="node" style="margin-top: 5px;text-align: center;color: #cccccc;height:50px;line-height:50px;cursor: pointer" @click="start">
        启动
      </div>

      <div v-if="isRun==true" class="node" style="margin-top: 5px;text-align: center;color: #cccccc;height:50px;line-height:50px;cursor: pointer" @click="end">
        暂停
      </div>

    </div>

<!--    <div style="width: 250px;height: 60px;position: fixed;left:70px;top:50px;background-color: #111217">
      <div style="color:#FFFFFF;font-size: 30px">欢迎来到监控界面</div>
    </div>-->

      <iframe :src="urlStr" style="height: 100vh;width:100%;border: medium none" ></iframe>


  </div>
</template>

<script>
import request from "@/utils/request";
import axios from 'axios'

export default {
  name: "monitor",
  data(){
    return{
      isRun:true,
      urlStr:'',
    }

  },
  created() {
    this.load();
  },
  methods:{
    load(){
      this.urlStr=sessionStorage['urlStr'];

      //this.urlStr="http://172.16.20.190:3000/d/dAh43sVnk/k8s-podjian-kong?orgId=1&var-CPU_NAME=EXPC"+task_id+"&var-GPU_NAME=EXPG"+task_id+"&refresh=5s"

      request.get("api/ifMonitorNode").then(res=>{
        console.log(res);
        if(res.code=='200'){
          if(res.data=="True"){
            this.isRun=true;
          }else{
            this.isRun=false;
          }
        }else{
          this.$message({ type:"success", message:data.msg });
        }
      })
    },
    start(){
      request.get("api/startMonitorNode").then(res=>{

        if(res.code=='200'){
          this.$message({ type:"success", message:"已开启" });
          this.isRun=true;
        }else{
          this.$message({ type:"success", message:data.msg });
        }
      })

    },
    end(){
      request.get("api/endMonitorNode").then(res=>{

        if(res.code=='200'){
          this.isRun=false;
          this.$message({ type:"success", message:"已暂停" });
        }else{
          this.$message({ type:"success", message:data.msg });
        }
      })

    }


  }
}


</script>

<style scoped>

.node:hover{
  background-color: #22252B;
}



</style>