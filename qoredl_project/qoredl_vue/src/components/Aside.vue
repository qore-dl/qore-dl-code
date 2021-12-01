<template>
	
	<div style="">
		<!--  -->

		<el-menu
			  style="height: 100vh;"
		      :default-active="path"
			  router
		      class="el-menu-vertical-demo"
        background-color="#304156"
        text-color="#BFCBD9"
        active-text-color="#3F9EFF"
        :default-openeds="['1',]"
    >
		      <el-submenu index="1" >
				  
				  <template slot="title">
					<i class="el-icon-location"></i>
					<span>系统管理</span>
				  </template>

            <el-menu-item index="/dashboard"><i class="el-icon-eleme"></i>主面板</el-menu-item>
            <el-menu-item index="/monitor"><i class="el-icon-eleme"></i>资源监控</el-menu-item>


          </el-submenu>
			  
		    </el-menu>
	</div>
</template>

<script>
export default{
	name:"Aside",
	data(){
		return{
			path:this.$route.path,
      isCollapse:false,
		}
	}
}
	
	
</script>

<style>
.el-menu{
  border-right-width: 0;
}

</style>
