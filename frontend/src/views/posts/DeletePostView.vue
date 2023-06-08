<template>
    <div class="container d-flex justify-content-center mt-5">
        <div class="col-lg-6 col-md-8 col-sm-10" style="margin-top:50px">
            <h5 class="text-center">Delete Post</h5>

            <p class="text-center" style="font-size:16px">Press the delete button in order to delete the post.</p>
            <hr>

            <div class="form-group d-flex justify-content-center">
                <p style="font-size:17px;margin-top:20px">Are you sure you want to delete this post ??</p>
            </div>

            <div class="form-group d-flex justify-content-center">
                <button @click="deletePost" class="btn btn-outline-danger">Delete Post</button>

                <router-link :to="{ name: 'Profile-Page', params: { username: profile.username } }" class="btn btn-outline-secondary ml-2"
                    style="margin-left: 10px;">Cancel</router-link>
            </div>

            
        </div>
    </div>
</template>


<script>
import axios from 'axios'
import refreshAccessToken from '@/utils/refresh_token.js';

export default {
    name: 'DeletePostView',

    data() {
        return {
            profile: {
                username: '',
            },
        }
    },

    methods: {
        async deletePost() {
            const post_id = this.$route.params.post_id

            try {
                let access_token = localStorage.getItem('access_token')
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                // Send a DELETE request to the server to delete the post.
                await axios.delete(`http://127.0.0.1:5000/api/post/${post_id}`)

                this.$router.push('/feed')

            } catch (error) {
                if (error.response.status === 401) {
                    await refreshAccessToken()
                    await this.deletePost()
                }

                else if (error.response.status === 403) {
                    alert('You are not authorized to delete this post.')
                }

                else {
                    console.error(error)
                    alert('An error occurred while deleting the post.')
                }
            }
        }
    }
}
</script>


