<template>
  <div style="height:100vh;background: linear-gradient(#141e30, #243b55);" >

    <login-header></login-header>

    <div class="loginBox">
      <h2>reset password</h2>

        <div class="item">
          <input type="text" required v-model="form.sendTo">
          <label for="">email</label>
        </div>

        <div class="item">

          <div style="display: flex;justify-content: space-between;">

            <div>
              <input type="text" required v-model="form.code">
              <label for="">code</label>
            </div>

            <div>
              <el-button type="primary" @click="getCode">send code</el-button>
            </div>

          </div>
        </div>


        <div class="item">
          <input type="password" required v-model="form.password">
          <label for="">password</label>
        </div>


        <button class="btn" @click="resetPass">submit
          <span></span>
          <span></span>
          <span></span>
          <span></span>
        </button>


    </div>

  </div>


</template>

<script>
import request from "@/utils/request";
import loginHeader from "../../components/LoginHeader";

export default {
  name: "ForgetPass",
  components:{
    'loginHeader':loginHeader,
  },

  data(){
    return{
      form:{
      },

    }
  },
  methods:{
    getCode(){
      console.log("getcode");

      request.post("api/getVerifyCode",this.form).then(res=>{

        if(res.code=='200'){
          this.$message({ type:"success", message:res.msg });

          //this.$router.push("/");//登录成功跳转
        }else{
          //console.log(res);
          this.$message({ type:"error", message:res.msg });
        }
      })


    },
    resetPass(){

      console.log("reset");

      request.post("api/resetPassword",this.form).then(res=>{

        if(res.code=='200'){
          this.$message({ type:"success", message:res.msg });

          //this.$router.push("/");//登录成功跳转
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

a {
  text-decoration: none;
}

input,
button {
  background: transparent;
  border: 0;
  outline: none;
}


body {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 16px;
  background-color: red;
}

.loginBox {
  width: 400px;
  height: 430px;
  background-color: #0c1622;
  margin: 100px auto;
  border-radius: 10px;
  box-shadow: 0 15px 25px 0 rgba(0, 0, 0, .6);
  padding: 40px;
  box-sizing: border-box;
}

h2 {
  text-align: center;
  color: aliceblue;
  margin-bottom: 30px;
  font-family: 'Courier New', Courier, monospace;
}

.item {
  height: 45px;
  border-bottom: 1px solid #fff;
  margin-bottom: 40px;
  position: relative;
}

.item input {
  width: 100%;
  height: 100%;
  color: #fff;
  padding-top: 20px;
  box-sizing: border-box;
}

.item input:focus+label,
.item input:valid+label {
  top: 0px;
  font-size: 2px;
}

.item label {
  position: absolute;
  left: 0;
  top: 12px;
  transition: all 0.5s linear;
  color: #03e9f4;
}

.btn {
  padding: 10px 20px;
  margin-top: 30px;
  color: #03e9f4;
  position: relative;
  overflow: hidden;
  text-transform: uppercase;
  letter-spacing: 2px;
  left: 35%;
}

.btn:hover {
  border-radius: 5px;
  color: #fff;
  background: #03e9f4;
  box-shadow: 0 0 5px 0 #03e9f4,
  0 0 25px 0 #03e9f4,
  0 0 50px 0 #03e9f4,
  0 0 100px 0 #03e9f4;
  transition: all 1s linear;
}

.btn>span {
  position: absolute;
}

.btn>span:nth-child(1) {
  width: 100%;
  height: 2px;
  background: -webkit-linear-gradient(left, transparent, #03e9f4);
  left: -100%;
  top: 0px;
  animation: line1 1s linear infinite;
}

@keyframes line1 {

  50%,
  100% {
    left: 100%;
  }
}

.btn>span:nth-child(2) {
  width: 2px;
  height: 100%;
  background: -webkit-linear-gradient(top, transparent, #03e9f4);
  right: 0px;
  top: -100%;
  animation: line2 1s 0.25s linear infinite;
}

@keyframes line2 {

  50%,
  100% {
    top: 100%;
  }
}

.btn>span:nth-child(3) {
  width: 100%;
  height: 2px;
  background: -webkit-linear-gradient(left, #03e9f4, transparent);
  left: 100%;
  bottom: 0px;
  animation: line3 1s 0.75s linear infinite;
}

@keyframes line3 {

  50%,
  100% {
    left: -100%;
  }
}

.btn>span:nth-child(4) {
  width: 2px;
  height: 100%;
  background: -webkit-linear-gradient(top, transparent, #03e9f4);
  left: 0px;
  top: 100%;
  animation: line4 1s 1s linear infinite;
}

@keyframes line4 {

  50%,
  100% {
    top: -100%;
  }
}


</style>