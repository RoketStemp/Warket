<template>
   <div>
      {{product.name}}
      <div class="field has-addons mt-6">
         <div class="control">
            <input type="number" class="input" min="1" v-model="quantity">
         </div>
         <div class="control">
            <a class="button is-dark" @click="addToCart">Add to cart</a>
         </div>
      </div>
      <router-link :to="product.get_absolute_url+'comments'" class="button is-light">Comments</router-link>
   </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'

export default {
   name: "Product",
   data(){
      return{
         product:{},
         quantity: 1
      }
   },
   mounted(){
      this.getProduct();
   },
   methods:{
      getProduct(){
         const category_slug = this.$route.params.category_slug;
         const product_slug = this.$route.params.product_slug;

         axios
            .get(`/api/v1/products/${category_slug}/${product_slug}`)
            .then(response=>{
               this.product = response.data
            })
            .catch(error=>{
               console.log(error)
            })
      },
      addToCart(){
         if(isNaN(this.quantity) || this.quantity<1){
            this.quantity = 1
         }

         const item = {
            product: this.product,
            quantity: this.quantity
         }
         console.log(item)
         this.$store.commit('addToCart', item)

         toast({
            message: 'This product was added to the cart',
            type: 'is-success',
            dismissible: true,
            pauseOnHover: true,
            duration: 2000,
            position: 'bottom-right',
         })
      }
   }
}
</script>

<style lang="scss" scoped>

</style>