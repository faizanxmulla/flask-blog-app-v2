<template>
    <div class="container d-flex justify-content-center mt-5">

        <div class="col-lg-6 col-md-8 col-lg-6 col-sm-10" style="margin-top: 20px;">

            <h5 class="text-center">Update Comments.</h5>
                <p class="text-center"> Make changes to your comments.</p>
                <hr>

                <form @submit.prevent="updateComment()">

                    <div  class="form-group d-flex justify-content-center">

                        <textarea 
                            class="form-control" 
                            v-model="comment.content" 
                            placeholder="enter new comment ..." style="width:80%; margin-top:7PX" 
                            rows="4">
                        </textarea>

                        <div v-if="errors.content" class="text-danger">{{ errors.content }}</div>
                    </div>

                    <br>

                    <div class="form-group d-flex justify-content-center">

                        <button type="submit" class="btn btn-outline-primary" >Update</button>

                        <router-link :to="'/post/' + $route.params.post_id + '/comment'" class="btn btn-outline-secondary ml-2" style="margin-left: 6px;">Cancel</router-link>

                    </div>

                </form>
        </div>
        
    </div>
</template>

<script>
import axios from 'axios'
import refreshAccessToken from '@/utils/refresh_token.js'

export default {
    name: 'UpdateCommentView',
    data() {
        return {
            comment: {
                content: ''
            },
            errors: {}
        }
    },

    created() {
        // fetch the comment data for the given comment ID
        this.fetchCommentData()
    },

    methods: {
        async fetchCommentData() {
            const post_id = this.$route.params.post_id

            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                const response = await axios.get(`http://127.0.0.1:5000/api/post/${post_id}/comment`)

                this.comment = response.data


            } catch (error) {

                if (error.response && error.response.status === 401) {
                    await refreshAccessToken()
                    await this.fetchCommentData()
                }

                else {
                    console.error(error)
                    alert('An error occurred while fetching the comment data.')
                }
            }
        },


        async updateComment() {
            this.errors = {}

            let formData = new FormData();

            formData.append('data', JSON.stringify(this.comment))

            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                const post_id = this.$route.params.post_id
                const comment_id = this.$route.params.comment_id

                await axios.put(`http://127.0.0.1:5000/api/post/${post_id}/comment/${comment_id}`, formData)

                this.$router.push(`/post/${post_id}/comment`)

            } catch (error) {

                if (error.response && error.response.status === 401) {
                    await refreshAccessToken()
                    await this.updateComment()
                } 

                else if (error.response.status === 403) {
                    alert('You are not authorized to update this comment.')
                }

                else  {
                    this.errors = error.response.data.errors
                    alert('An error occurred while commenting on this post.')
                }
            }
        }
    }
}
</script>