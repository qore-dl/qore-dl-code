<template>
<div>
  <login-header></login-header>

  <div style="text-align: center;font-size: 40px">{{msg}}</div>

</div>
</template>

<script>
import request from "@/utils/request";

import loginHeader from "../../components/LoginHeader";


export default {
  name: "Activate",
  components:{
    'loginHeader':loginHeader,
  },
  created() {
    let code=this.$route.query.code;
    request.post("api/activate",{code:code}).then(res=>{

      if(res.code=='200'){

      }else{
        this.msg="激活失败,请重新再试"
      }
    })

  },

  data(){
    return{
      msg:'激活成功,请登录'
    }
  },
  methods:{

  },


}



</script>

<style scoped>


</style>