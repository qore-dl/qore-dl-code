import Vue from 'vue'
import VueRouter from 'vue-router'
import { Message } from 'element-ui';

Vue.use(VueRouter)

const routes = [

  {
    path: '/',
    name: 'Layout',
    component: () => import( '../layout/Layout.vue'),
    redirect:"/monitor",
    children:[
      {
        path: '/dashboard',
        name: 'dashboard',
        component: () => import( '../views/Dashboard')
      },
      {
        path: '/monitor',
        name: 'monitor',
        component: () => import( '../views/Monitor')
      },
      {
        path: '/taskmonitor',
        name: 'taskmonitor',
        component: () => import( '../views/TaskMonitor')
      },
      {
        path: '/test',
        name: 'test',
        component: () => import( '../views/Test')
      },
      {
        path: '/taskmanage',
        name: 'taskmanage',
        component: () => import( '../views/TaskManage')
      },
      {
        path: '/imagemanage',
        name: 'imagemanage',
        component: () => import( '../views/ImageManage')
      },

      {
        path: '/uploadtask',
        name: 'uploadtask',
        component: () => import( '../views/UploadTask')
      },

    ]

  },
  {
    path: '/login',
    name: 'Login',
    component: () => import( '../views/loginEtc/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import( '../views/loginEtc/Register.vue')
  },
  {
    path: '/forgetpass',
    name: 'forgetpass',
    component: () => import( '../views/loginEtc/ForgetPass.vue')
  },
  {
    path: '/activate',
    name: 'activate',
    component: () => import( '../views/loginEtc/Activate.vue')
  },


]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  if (to.path === '/login' ||to.path==='/register'||to.path==='/forgetpass'||to.path==='/activate') {
    next();
  } else {

    let Token = localStorage.getItem('Token');
    if (Token == null || Token === '') {
      Message.error("登录过期");
      next('/login');
    } else {
      next();
    }
  }
});

export default router
