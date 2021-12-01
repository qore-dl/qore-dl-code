<template>
  <div>
    <div>系统管理</div>
    <el-button @click="test">按钮1</el-button>
    <el-button @click="test2">按钮2</el-button>
    <el-button @click="test2">按钮3</el-button>

  </div>
</template>

<script>
import request from "@/utils/request";
import axios from 'axios'


export default {
  name: "Test",
  methods: {
    test(){
/*      request.post("/test1").then(res=>{
        if(res.code=='200'){
          this.$message({ type:"success", message:"登录成功" });
        }else{
          this.$message({ type:"error", message:res.msg });
        }
      })*/

      axios.get("/flaskapi/monitor/ifMonitorNode").then(res=>{
        console.log(res);
      })

    },
    test2(){
      axios.post("/api/Login").then(res=>{

        if(res.code=='200'){
          this.$message({ type:"success", message:"登录成功" });

        }else{
          //console.log(res);
          this.$message({ type:"error", message:res.msg });
        }
      })
    }

  },


}
</script>

<style scoped>

</style>