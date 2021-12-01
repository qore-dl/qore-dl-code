<template>
	<div >
		<!-- 头部 -->
		<Header class="header"></header>
<!--		<div style="display: flex;">
			<Aside class="aside"></Aside>
			<div class="content" ><router-view style="flex: 1;"/></div>
		</div>-->
    <div class="content" ><router-view/></div>

	</div>
</template>

<script>
	import Header from "@/components/Header";
	import Aside from "@/components/Aside";
		
	export default{
		name:"Layout",
		components:{
			Header,Aside
		}
	}
</script>

<style scoped>
	.header{
	  width:100%;
	  height:50px;
	  background: #fff;
	  position:fixed;
	}

  .content{
    position:absolute;
    left:0;
    top:50px;
    bottom: 0;
    width:100%;
    overflow: auto;
  }


</style>
