<template>
    <div class="page-search">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Search</h1>
                <h2 class="is-size-5 has-text-centered">
                    Search term: "{{ query }}"
                </h2>
            </div>
            <product-box 
              v-for="product in products"
              :key="product.id"
              :product="product"
            />
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import ProductBox from '../components/ProductBox.vue'

export default {
    components:{
        ProductBox
    },
    data () {
        return {
            products: [],
            query: ''
        }
    },
    mounted() {
        let uri = window.location.search.substring(1)
        let params = new URLSearchParams(uri)

        if (params.get('query')) {
            this.query = params.get('query')
            this.performSearch()
        }
    },
    methods: {
        async performSearch() {
            await axios
                .post('/api/v1/products/search/', {'query': this.query})
                .then(response => {
                    this.products = response.data
                    console.log(this.products)
                })
                .catch(error => {
                    console.log(error)
                })
        }
    }
}
</script>
