import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/Login.vue'
import Navigation from '../views/Navigation.vue'
import Project from '../components/project/Project.vue'
import Module from '../components/module/Module.vue'
import CaseList from '../components/case/CaseList.vue'
import Task from '../components/task/Task.vue'
import ReportList from '../components/report/ReportList.vue'


Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/main',
    name: 'Navigation',
    component: Navigation,
    children: [
      {
        // 当 /main/project 匹配成功，
        // project 会被渲染在 Navigation 的 <router-view> 中
        path: 'project',
        component: Project
      },
      {
        path: 'module',
        component: Module
      },
      {
        path: 'case',
        component: CaseList
      },
      {
        path: 'task',
        component: Task
      },
      {
        path: 'report',
        component: ReportList
      }
    ]
  },

]

const router = new VueRouter({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes
})

// 导航守卫，控制一些页面登录才能访问
router.beforeEach((to, from, next) => {
  if (to.path === '/login') { // 当路由为login时就直接下一步操作
    next();
  } else { // 否则就需要判断
    if(sessionStorage.token){ // 如果有用户名就进行下一步操作
      next()
    }else{
      next({path: '/login'}) // 没有用户名就跳转到login页面
    }
  }
});

export default router
