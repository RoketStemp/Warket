import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/Home.vue'
import Product from '../views/Product.vue'
import Category from '../views/Category.vue'
import Cart from '../views/Cart.vue'
import Login from '../views/Login.vue'
import Signup from '../views/Signup.vue'
import Comments from '../views/Comments.vue'
import Search from '../views/Search.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/:category_slug/:product_slug/comments',
    name: 'Comments',
    component: Comments
  },
  {
    path: '/:category_slug/:product_slug',
    name: 'Product',
    component: Product
  },
  {
    path: '/:category_slug',
    name: 'Category',
    component: Category
  },
  {
    path: '/search',
    name: 'Search',
    component: Search
  },
  {
    path: '/cart',
    name: 'Cart',
    component: Cart
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Signup
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if(to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated){
    next({name: 'LogIn', query: {to: to.path} });
  }else{
    next()
  }
})

export default router
