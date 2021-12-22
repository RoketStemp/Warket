<template>
  <div>
    <div class="navbar is-dark" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <a class="navbar-item" href="/">
          Warket
        </a>

        <a class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbar-menu" @click="showMobileMenu = !showMobileMenu">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div id="navbarBasicExample" class="navbar-menu" v-bind:class="{'is-active': showMobileMenu}">
        <div class="navbar-start">
            <div class="navbar-item">
               <form method='get' action="/search">
                <div class="field has-addons">
                  <input type="text" class="input" placeholder="What are you looking for?" name="query"/>

                  <div class="control">
                    <button class="button is-success">
                      <span class="icon">
                        <i class="fas fa-search"></i>
                      </span>
                    </button>
                  </div>
                </div>
               </form>
            </div>

          <div class="navbar-item has-dropdown is-hoverable">
            <a class="navbar-link">
              Categories
            </a>

            <div class="navbar-dropdown">
              <a class="navbar-item" href="/computers">
                Computers
              </a>
              <a class="navbar-item" href="/laptops">
                Laptops
              </a>
            </div>
          </div>
        </div>

        <div class="navbar-end">

            <div class="navbar-item">
              <div class="buttons">
                <template v-if="$store.state.isAuthenticated">
                  <router-link to="/my-account" class="button is-light">My account</router-link>
                </template>

                <template v-else>
                  <router-link to="/log-in" class="button is-light">Log in</router-link>
                </template>

                <router-link to="/cart" class="button is-success">
                  <span class="icon"><i class="fas fa-shopping-cart"></i></span>
                  <span>Cart ({{ cartTotalLength }})</span>
                </router-link>
              </div>
            </div>
          </div>
      </div>

      
    </div>
    <div id="content">
      <router-view/>
    </div>
    
  </div>
  
</template>

<script>
import axios from 'axios'
import Modal from './components/Modal.vue'

export default {
  
  data(){
    return{
      showMobileMenu: false,
      cart: {
        items: []
      }
    }
  },
  beforeCreate(){
    this.$store.commit('initializeStore')

    const token = this.$store.state.token

    if(token){
      axios.defaults.headers.common['Authorization'] = "Token " + token
    } else {
      axios.defaults.headers.common['Authorization'] = ""
    }
  },
  mounted(){
    this.cart = this.$store.state.cart
  },
  computed: {
    cartTotalLength(){
      let totalLength = 0

      for (let i = 0; i < this.cart.items.length; i++) {
        totalLength += this.cart.items[i].quantity
      }

      return totalLength
    }
  }
}

</script>

<style lang="scss">
@import '../node_modules/bulma';
#content{
  margin: 20px;
}
</style>
