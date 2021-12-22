<template>
    <div class="column is-3">
      <div class="box">
        
        <figure class="image mb-4">
          <img :src="product.get_image" alt="product image">
          <label class="checkbox comparingCheckbox">
            <fieldset :id="'fieldset'+product.id">
              <input type="checkbox" class='check' :value="product.id" @change="$emit('wasSelected', $event.target.checked)">
            </fieldset>
            
          </label>
        </figure>

        <h3 class="is-size-4">{{ product.name }}</h3>
        <p class="is-size-6 has-text-grey">${{ product.price }}</p>

        <router-link :to="product.get_absolute_url" class="button is-dark mt-4">View Details</router-link>
      </div>
    </div>
</template>

<script>
export default {
    name: 'ProductBox',
    props: {
        product: Object
    }
}
</script>

<style scoped>
.checkbox{
  position: absolute;
  z-index: 10;
  top: 7px;
  right:7px;
}
.comparingCheckbox{
  display: none;
}
.check{
  height: 25px;
  width: 25px;
}
.image{
  margin-top: -1.25em;
  margin-left: -1.25em;
  margin-right: -1.25em;
}
</style>