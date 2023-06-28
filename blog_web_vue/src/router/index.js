import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import PersonalPage from '../views/PersonalPage'
import Write from '../views/Write.vue'
import ArticleDetails from '../views/ArticleDetails.vue'
import Filing from '../views/Filing.vue'
import Edit from '../views/Edit.vue'
import Update from '../views/Update.vue'
import Editcomment from '../views/Editcomment.vue'
Editcomment
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path:'/ArticleDetails',
    name:'ArticleDetails',
    component: ArticleDetails
    
  },
  {
    path: '/PersonalPage',
    name: 'PersonalPage',
    component: PersonalPage
  },
  {
    path: '/Write',
    name: 'Write',
    component: Write
  },
  {
    path: '/Filing',
    name: 'Filing',
    component: Filing
  },
  {
    path: '/Edit',
    name: 'Edit',
    component: Edit
  },
  {
    path: '/Update',
    name: 'Update',
    component: Update
  },

  {
    path: '/Editcomment',
    name: 'Editcomment',
    component: Editcomment
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
