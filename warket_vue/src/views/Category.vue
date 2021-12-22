<template>
    <div>
        <div class="columns is-multiline">
            <div class="column is-12">
                <h2 class="is-size-2 has-text-centered">Latest {{this.$route.params.category_slug}}</h2>
                <button v-if="!selectComparing" class="button is-dark mt-4 ml-4" @click="showCheckboxes()">Select to compare</button>
                <button v-if="selectComparing" class="button is-dark mt-4 ml-4" @click="openComparingModal()">Compare</button>
            </div>
            
            <product-box
            v-for="product in category.products"
            :key="product.id"
            :product="product"
            @wasSelected='checkLength'
            />
        </div>
        <comparing-modal
            :class='{"is-active": showModalWindow}'
            :products="selected"
            :prices="prices"
            :rams="rams"
            :videos="videos"
            :batteries="batteries"
            @close='showModalWindow=!showModalWindow'
        />
    </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'

import ProductBox from '../components/ProductBox.vue'
import ComparingModal from '../components/ComparingModal.vue'

export default {
    name: 'Category',
    data(){
        return{
            category: {
                products: []
            },
            selectComparing: false,
            selected:[],
            length:0,
            showModalWindow: false,
            prices: [],
            rams: [],
            videos: [],
            batteries: [],
        }
    },
    components: {
        ProductBox,
        ComparingModal
    },
    mounted(){
        this.getProductsByCategory()
    },
    watch: {
        $route(to, from) {
            if(to.name == 'Category'){
                this.getProductsByCategory()
            }
        }
    },
    methods: {
        getProductsByCategory(){
            const category_slug = this.$route.params.category_slug

            axios
                .get(`api/v1/products/${category_slug}`)
                .then(response => {
                    this.category.products = response.data
                })
                .catch(error => {
                    console.log(error)

                    toast({
                        message: 'Something went wrong. Please try again.',
                        type: 'is-danger',
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 2000,
                        position: 'bottom-right',
                    })
                })
            
        },
        showCheckboxes(){
            let checkboxes = Array.prototype.slice.call(document.getElementsByClassName('comparingCheckbox'))
            checkboxes.forEach(checkbox => {
                checkbox.style.display = 'block'
            });
            this.selectComparing = true
        },
        openComparingModal(){
            this.selected = []
            let counter = 0
            
            let checkboxes = Array.prototype.slice.call(document.getElementsByClassName('comparingCheckbox'))
            checkboxes.forEach(checkbox => {
                if(checkbox.children[0].children[0].checked === true){
                    this.selected.push(this.category.products[counter])
                    if(this.category.products[counter].category==='computers'){
                        this.prices.push(parseInt(this.category.products[counter].price))
                        this.rams.push(parseInt(this.category.products[counter].ram))
                        this.videos.push(parseInt(this.category.products[counter].video))
                    }else{
                        this.prices.push(parseInt(this.category.products[counter].price))
                        this.rams.push(parseInt(this.category.products[counter].ram))
                        this.videos.push(parseInt(this.category.products[counter].video))
                        this.batteries.push(parseInt(this.category.products[counter].battery))
                    }
                }
                counter++
            });
            [this.prices,this.rams,this.videos,this.batteries] = this.selectMinAndMax(this.prices,this.rams,this.videos,this.batteries)
            if(this.selected.length<2){
                toast({
                    message: 'Please choose at least 2 products!',
                    type: 'is-danger',
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 3000,
                    position: 'bottom-right',
                })
            }else{
                this.showModalWindow = true
            }
            
        },
        checkLength(checked){
          if((this.length+1)===4 && checked){
            let checkboxes = Array.prototype.slice.call(document.getElementsByClassName('comparingCheckbox'))
            checkboxes.forEach(checkbox => {
                if(checkbox.children[0].children[0].checked !== true){
                    let fieldset = document.getElementById('fieldset'+checkbox.children[0].children[0].value)
                    fieldset.setAttribute('disabled', true);
                }
            });
            this.length++
          } else if(this.length===4 && !checked){
            let checkboxes = Array.prototype.slice.call(document.getElementsByClassName('comparingCheckbox'))
            checkboxes.forEach(checkbox => {
                if(checkbox.children[0].children[0].checked !== true){
                    let fieldset = document.getElementById('fieldset'+checkbox.children[0].children[0].value)
                    fieldset.removeAttribute('disabled');
                }
            });

            this.length--
          } else if(checked) {
            this.length++
          } else{
            this.length--
          }
        },
        selectMinAndMax(...arrays){
            arrays.forEach(arr => {
                arr.sort(function(a, b) { return a-b})
            })
            return arrays
        }
    }
}

</script>

<style lang="scss" scoped>

</style>