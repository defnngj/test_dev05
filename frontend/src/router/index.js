import Vue from 'vue'
import VueRouter from 'vue-router'
import Project from '../components/project/Project.vue'
import Module from '../components/module/Module.vue'
import CaseList from '../components/case/CaseList.vue'
import Task from '../components/task/Task.vue'


Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Project',
    component: Project
  },
  {
    path: '/module',
    name: 'Module',
    component: Module
  },
  {
    path: '/case',
    name: 'CaseList',
    component: CaseList
  },
  {
    path: '/task',
    name: 'Task',
    component: Task
  },
  // {
  //   path: '/about',
  //   name: 'About',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  // }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
