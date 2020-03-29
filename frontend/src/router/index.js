import Vue from 'vue'
import VueRouter from 'vue-router'
import Layout from '../layout/index.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: Layout,
    redirect: '/industries',
    children: [
      {
        path: 'industries',
        name: 'IndustryList',
        component: () => import('../views/IndustryList'),
        meta: { title: '行业列表' }
      },
      {
        path: 'industries/:id',
        name: 'Industry',
        props: true,
        component: () => import('../views/Industry'),
        meta: { title: '行业' }
      },
      {
        path: 'compare',
        name: 'Compare',
        component: () => import('../views/Compare'),
        meta: { title: '对比' }
      }
    ]
  },
  // {
  //  path: '/about',
  //  name: 'About',
  // route level code-splitting
  // this generates a separate chunk (about.[hash].js) for this route
  // which is lazy-loaded when the route is visited.
  //  component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  // }

  // 404 page must be placed at the end !!!
  { path: '*', component: () => import('../views/404') }
]

const router = new VueRouter({
  routes
})

export default router
