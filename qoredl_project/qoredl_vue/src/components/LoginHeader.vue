<template>
  <div style="height: 50px;line-height: 50px; display: flex; background-color: #333333" >

    <div style="width: 250px; padding-left: 30px; font-weight: bold; color: skyblue;">

      <svg class="icon" aria-hidden="false" style="font-size: 40px">
        <use xlink:href="#icon-suanfa"></use>
      </svg>
      智能计算服务系统
    </div>

    <div style="flex: 1"></div>

    <div style="width: 50px;color: #FFFFFF;cursor: pointer" @click="$router.replace('/login')">
      登录
    </div>
    <div style="width: 50px;color: #FFFFFF;cursor: pointer" @click="$router.replace('/register')">
      注册
    </div>

  </div>
</template>

<script>
export default {
  name: "LoginHeader"
}
</script>

<style scoped>

</style>