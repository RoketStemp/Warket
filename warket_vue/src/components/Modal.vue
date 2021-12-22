<template>
    <div class="modal">
        <div class="modal-background"></div>
        <div class="modal-content">
            <div class="column is-12 box">
                <h2 class="subtitle">{{title}}</h2>

                <p class="has-text-grey mb-4">* All fields are required</p>

                <div class="columns is-multiline">
                    <div class="column is-12"  v-for="field in fields" :key='field'>
                        <div class="field">
                            <label>{{field.title}}</label>
                            <div class="control">
                                <input type="text" class="input" v-model="field.value">
                            </div>
                        </div>
                    </div>
                </div>

                <div class="notification is-danger mt-4" v-if="errors.length">
                    <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                </div>

                <hr>
                <template v-if="type_modal==='addComment'">
                    <button class="button is-dark" @click="addComment()">Add</button>
                </template>
                <template v-if="type_modal==='editComment'">
                    <button class="button is-dark" @click="editComment()">Edit</button>
                </template>
                <template v-if="type_modal==='addReply'">
                    <button class="button is-dark" @click="addReply()">Add</button>
                </template>
            </div>
        </div>
        <button class="modal-close is-large" aria-label="close" @click="$emit('close')"></button>
    </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'

export default {
    name: 'Modal',
    props: {
        type_modal: String,
        target_id: Number,
        comment_data: Object,
    },
    data(){
        return{
            fields:{},
            title:'',
            errors: [],
        }
    },
    watch:{
        type_modal:{
            immediate: true, 
            handler (type, oldType) {
                if(type === 'addComment'){
                    this.title = 'Create Comment'
                    this.fields={
                        'text': {
                            'title': 'Text *',
                            'value': ''
                        },
                        'rating': {
                            'title': 'Rating',
                            'value': ''
                        },
                        'advantages': {
                            'title': 'Advantages',
                            'value': ''
                        },
                        'disadvantages': {
                            'title': 'Disadvantages',
                            'value': ''
                        }
                    }
        
                }else if(type === 'editComment'){
                    this.title = 'Edit Comment'
                    this.fields={
                        'text': {
                            'title': 'Text *',
                            'value': this.comment_data.text
                        },
                        'rating': {
                            'title': 'Rating',
                            'value': this.comment_data.rating
                        },
                        'advantages': {
                            'title': 'Advantages',
                            'value': this.comment_data.advantages
                        },
                        'disadvantages': {
                            'title': 'Disadvantages',
                            'value': this.comment_data.disadvantages
                        }
                    }
        
                }
                else if(type === 'addReply'){
                    this.title = 'Add reply'
                    this.fields={
                        'text': {
                            'title': 'Enter your reply *',
                            'value': this.comment_data.text
                        },
                    }
        
                }
            }
        }
    },
    methods: {
        addComment(){
           const category_slug = this.$route.params.category_slug;
           const product_slug = this.$route.params.product_slug;

           this.errors = []
            if (this.text === '') {
                this.errors.push('The text field is missing!')
            }

            if (!this.errors.length) {
                
                const data = {
                    'text': this.fields.text.value,
                    'rating': this.fields.rating.value,
                    'advantages': this.fields.advantages.value,
                    'disadvantages': this.fields.disadvantages.value,
                }
                axios
                    .post(`/api/v1/products/${category_slug}/${product_slug}/comments/add`, data)
                    .then(response=>{

                        this.$emit('update', response)
                        this.$emit('close')
                    })
                    .catch(error=>{
                        if(error.response) {
                            for(const property in error.response.data) {
                                this.errors.push(`${property}: ${error.response.data[property]}`)
                            }
                        }else{
                            this.errors.push('Something went wrong. Please try again')

                            console.log(JSON.stringify(error))
                        }
                    })
            }
      },
      editComment(){
            const category_slug = this.$route.params.category_slug;
            const product_slug = this.$route.params.product_slug;

            const data = {
                'id':this.target_id,
                'text': this.fields.text.value,
                'rating':this.fields.rating.value,
                'advantages': this.fields.advantages.value,
                'disadvantages': this.fields.disadvantages.value,
            }

          axios
            .post(`/api/v1/products/${category_slug}/${product_slug}/comments/edit`, data)
            .then(response=>{
                this.$emit('update', response)
                this.$emit('close')
            })
            .catch(error=>{

                toast({
                    message: 'Something went wrong. Please try again!',
                    type: 'is-danger',
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 2000,
                    position: 'bottom-right',
                })

                console.log(error)
            })

            this.showModalWindow = !this.showModalWindow
      },
      addReply(){
            const category_slug = this.$route.params.category_slug;
            const product_slug = this.$route.params.product_slug;

        const data = {
            'id':this.target_id,
            'text': this.fields.text.value,
        }

        axios
            .post(`/api/v1/products/${category_slug}/${product_slug}/comments/add_reply`, data)
            .then(response=>{
                this.$emit('update', response)
                this.$emit('close')
            })
            .catch(error=>{

                toast({
                    message: 'Something went wrong. Please try again!',
                    type: 'is-danger',
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 2000,
                    position: 'bottom-right',
                })

                console.log(error)
            })
      }
    }
}
</script>

<style lang="scss" scoped>

</style>