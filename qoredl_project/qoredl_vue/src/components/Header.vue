<template>
	<div style="height: 50px;line-height: 50px; display: flex; background-color: #333333" >

		<div style="width: 250px; padding-left: 30px; font-weight: bold; color: skyblue;">

      <svg class="icon" aria-hidden="false" style="font-size: 40px">
        <use xlink:href="#icon-suanfa"></use>
      </svg>
    智能计算服务系统

    </div>
		<div style="flex: 1;">
      <el-menu

          class="el-menu-demo"
          mode="horizontal"
          router
          background-color="#333333"
          text-color="#848391"
          active-text-color="#fff">

        <el-menu-item style="height: 50px" index="/monitor">资源监控</el-menu-item>
        <el-menu-item style="height: 50px" index="/imagemanage">镜像管理</el-menu-item>
        <el-menu-item style="height: 50px" index="/taskmanage">任务管理</el-menu-item>

      </el-menu>

    </div>

<!-- <div style="width: 50px">
      <svg class="icon" aria-hidden="false" style="font-size: 35px;cursor:pointer;">
        <use xlink:href="#icon-a-010-bell"></use>
      </svg>
    </div>-->

		<div style="width: 100px;">
			
			<el-dropdown @command="handleCommand">

			  <span class="el-dropdown-link" >
          <svg class="icon" aria-hidden="false" style="font-size: 35px;cursor:pointer;">
              <use xlink:href="#icon-icon-test"></use>
           </svg>
          <i class="el-icon-arrow-down el-icon--right"></i>
			  </span>

			    <el-dropdown-menu slot="dropdown">
<!--			      <el-dropdown-item command="a">个人信息</el-dropdown-item>-->
			      <el-dropdown-item command="b">退出系统</el-dropdown-item>

			    </el-dropdown-menu>
			</el-dropdown>


		</div>
	</div>
</template>

<script>
	
export default {
  name: 'headers',
  methods:{
		exit(){
		  //退出登录，清空token
      console.log("dda");
		  localStorage.removeItem('Token');
		  localStorage.removeItem('user_id');
		  this.$router.push('/login');
		},
    handleCommand(command) {
      if(command=="b"){
        this.exit();
      }
    }
	}
}
</script>


<style >
	
</style>
