<template>
   <div>
    <button class="button" @click="showAddCommentModal()">Some</button>

        <modal 
          :class='{"is-active": showModalWindow}'
          :type_modal='type_modal'
          :target_id='target_id'
          :comment_data='comment_data'
          @close='closeModal'
          @update='updateCommentsList'
        />

    <div class="has-addons mt-6">
        <comment
          v-for="comment in comments"
          :key="comment.id"
          :comment="comment"
          @remove="removeComment"
          @edit="showEditCommentModal"
          @reply="showAddReplyModal"
        />
    </div>
   </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'
import Comment from '../components/Comment.vue'
import Modal from '../components/Modal.vue'

export default {
   name: "Comments",
   components: {
       Comment, 
       Modal
    },
   data(){
        return{
            comments:[], 
            showModalWindow: false,
            type_modal:'',
            target_id:0,
            comment_data:{}
        }
   },
   mounted(){
      this.getComments();
   },
   methods:{
        closeModal(){
            this.showModalWindow = false
        },
        showAddCommentModal(){
            this.type_modal = 'addComment'
            this.showModalWindow = true
            this.target_id = 0
            this.comment_data={}
        },
        showEditCommentModal(comment){
            this.showModalWindow = true
            this.type_modal = 'editComment'
            this.target_id = comment.id
            this.comment_data = this.comments.filter(i => i.id === this.target_id)[0]
        },
        showAddReplyModal(comment){
            this.showModalWindow = true
            this.type_modal = 'addReply'
            this.target_id = comment.id
            this.comment_data={}
        },
        updateCommentsList(response){
            if(this.type_modal === 'addReply'){
              let comment = this.comments.filter(i => i.id === this.target_id)[0]
              comment['comment'].unshift({
                  'id': response.data['id'],
                  'is_reply': true,
                  'username': response.data['username'],
                  'date_added': response.data['date_added'],
                  'text':  response.data['text'],
              })

            }else{
                this.comments.unshift({
                    'id': response.data['id'],
                    'comment': [],
                    'is_reply': false,
                    'username': response.data['username'],
                    'date_added': response.data['date_added'],
                    'text':  response.data['text'],
                    'rating':  response.data['rating'],
                    'advantages':  response.data['advantages'],
                    'disadvantages':  response.data['disadvantages'],
                })
            }
        
        },
        getComments(){
            const category_slug = this.$route.params.category_slug;
            const product_slug = this.$route.params.product_slug;

            axios
                .get(`/api/v1/products/${category_slug}/${product_slug}/comments`)
                .then(response=>{
                this.comments = response.data
                console.log(this.comments)
                })
                .catch(error=>{
                console.log(error)
                })
        },
        removeComment(comment){
            const category_slug = this.$route.params.category_slug;
            const product_slug = this.$route.params.product_slug;

            axios
                .post(`/api/v1/products/${category_slug}/${product_slug}/comments/delete`, {'id':comment.id})
                .then(()=>{
                    this.comments = this.comments.filter(i => i.id !== comment.id)
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
                
        },
   }
}
</script>

<style lang="scss" scoped>

</style>