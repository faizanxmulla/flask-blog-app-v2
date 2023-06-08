<template>
    <div class="container d-flex justify-content-center mt-5">
        <div class="col-lg-6 col-md-8 col-sm-10" style="margin-top:50px">
            <h5 class="text-center">Delete Comment</h5>

            <p class="text-center" style="font-size:16px">Press the delete button in order to delete the comment.</p>
            <hr>

            <div class="form-group d-flex justify-content-center">
                    <p style="font-size:17px;margin-top:20px">Are you sure you want to delete this comment ??</p>
            </div>

            <div class="form-group d-flex justify-content-center">
                <button @click="deleteComment" class="btn btn-outline-danger">Delete Comment</button>

                <router-link :to="'/post/' + $route.params.post_id + '/comment'" class="btn btn-outline-secondary ml-2"
                    style="margin-left: 10px;">Cancel</router-link>
            </div>

            
        </div>
    </div>
</template>


<script>
import axios from 'axios'
import refreshAccessToken from '@/utils/refresh_token.js';

export default {
    name: 'DeleteCommentView',
    methods: {
        async deleteComment() {
            // Get the Comment ID from the route params
            const post_id = this.$route.params.post_id
            const comment_id = this.$route.params.comment_id

            try {
                // Get the access token from localStorage
                let access_token = localStorage.getItem('access_token')

                // Set the Authorization header of the axios instance
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                // Send a DELETE request to the server to delete the comment
                await axios.delete(`http://127.0.0.1:5000/api/post/${post_id}/comment/${comment_id}`)

                // Redirect the user to the home page
                this.$router.push(`/post/${post_id}/comment`)

            } catch (error) {
                // Handle authentication errors.
                if (error.response.status === 401) {
                    await refreshAccessToken()
                    await this.deleteComment()
                }

                // Handle authorization errors.
                else if (error.response.status === 403) {
                    alert('You are not authorized to delete this comment.')
                }

                // Handle other errors.
                else {
                    console.error(error)
                    alert('An error occurred while deleting the comment.')
                }
            }
        }
    }
}
</script>


