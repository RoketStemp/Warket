<template>
<div class="modal">
    <div class="modal-background"></div>
    <div class="modal-content is-four-fifths">
        <div class="columns box">
            <div class="column ml-1" v-for="index in products.length" :key="index">
                <figure class="image mb-4">
                    <img :src="products[index-1].get_thumbnail" alt="product image">
                </figure>

                <h3 class="is-size-4 has-text-centered mb-3">{{products[index-1].name}}</h3>
                <table class="table is-fullwidth">
                <tbody>
                        <tr>
                            <td v-if="products[index-1].price==prices[0]" class="min">Price: ${{products[index-1].price}}</td>
                            <td v-else-if="products[index-1].price==prices[prices.length-1]" class="max">Price: ${{products[index-1].price}}</td>
                            <td v-else class='middle'>Price: ${{products[index-1].price}}</td>
                        </tr>
                        <tr>
                            <td v-if="products[index-1].ram==rams[0]" class="max">RAM: {{products[index-1].ram}}GB</td>
                            <td v-else-if="products[index-1].ram==rams[rams.length-1]" class="min">RAM: {{products[index-1].ram}}GB</td>
                            <td v-else class='middle'>RAM: {{products[index-1].ram}}GB</td>
                        </tr>
                        <tr>
                            <td v-if="products[index-1].video==videos[0]" class="max">Video: {{products[index-1].video}}GB</td>
                            <td v-else-if="products[index-1].video==videos[videos.length-1]" class="min">Video: {{products[index-1].video}}GB</td>
                            <td v-else class='middle'>Video: {{products[index-1].video}}GB</td>
                        </tr>
                        <tr v-if="products[index-1].category==='laptops'">
                            <td v-if="products[index-1].battery==batteries[0]" class="max">Battery: {{products[index-1].battery}}mAh</td>
                            <td v-else-if="products[index-1].battery==batteries[batteries.length-1]" class="min">Battery: {{products[index-1].battery}}mAh</td>
                            <td v-else class='middle'>Battery: {{products[index-1].battery}}mAh</td>
                        </tr>
                        
                </tbody>
            </table>
            </div>
        </div>
    </div>
    <button class="modal-close is-large" aria-label="close" @click="$emit('close')"></button>
</div>
</template>

<script>
    export default {
        name: 'ComparingModal',
        props:{
            products: Array,
            prices: Array,
            rams: Array,
            videos: Array,
            batteries: Array,
        }
    }
</script>

<style lang="scss" scoped>
.min{
    background-color: green;
}
.max{
    background-color: red;
}
.middle{
    background-color: yellow;
}
.modal-content::-webkit-scrollbar {
  display: none;
}
.modal-content {
  -ms-overflow-style: none;  
  scrollbar-width: none;  
  overflow-x: hidden;
}
</style>