<template>
    <div class="columns">
      <div class="column is-11">
        <div class="box" v-if="comment.is_reply === false">
          <div>
            <p>{{comment.username}}</p>   
            {{comment.text}}
          </div>
          
          <div class="block">
              <div class='comment' v-for="reply in comment.comment" :key="reply">
              <div v-if="reply.is_reply === true">
                <p>{{reply.username}}</p>   
                {{reply.text}}
              </div>
          </div>
          </div>
          

          <button class="button is-danger" @click="$emit('remove', comment)"><i class="fas fa-eraser"></i></button>
          <button class="button is-success" @click="$emit('edit', comment)"><i class="fas fa-edit"></i></button>
          <button class="button is-success" @click="$emit('reply', comment)"><i class="fas fa-reply"></i></button>
        </div>
      </div>
    </div>
</template>

<script>
export default {
    name: 'Comment',
    props: {
        comment: Object
    },
}
</script>

<style scoped>
.column{
  margin: auto;
}
.block{
  padding-left: 15px;
  border-left: 1px solid gray;
}
.comment{
  margin-top: 15px;
}
</style>