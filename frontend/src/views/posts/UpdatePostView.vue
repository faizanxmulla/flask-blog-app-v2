<template>
    <div class="container d-flex justify-content-center mt-5">
        <div class="col-lg-6 col-md-8 col-sm-10" style="margin-top: 10px;">
            <h5 class="text-center">Update Post</h5>
            <p class="text-center"> Fill the form to update an existing post.</p>
            <hr>

            <form @submit.prevent="updatePost()" enctype="multipart/form-data">

                <div class="form-group" style="display: flex; flex-direction: column; align-items: center;">

                    <label for="post.title">Title</label>

                    <input type="text" class="form-control" v-model="post.title" placeholder="Enter title (required)" style="width:80%; margin-top:5px"/>

                    <div v-if="errors.title" class="text-danger">{{ errors.title }}</div>
                </div>

                <br>

                <div class="form-group" style="display: flex; flex-direction: column; align-items: center;">

                    <label for="caption">Caption</label>

                    <textarea 
                        class="form-control" 
                        v-model="post.caption" 
                        placeholder="Enter Caption / Description" style="width:80%; margin-top:7px" 
                        rows="6"></textarea>

                    <div v-if="errors.caption" class="text-danger">{{ errors.caption }}</div>

                </div>

                <br>

                <div class="form-group" style="display: flex; flex-direction: column; align-items: center;">

                    <label for="image">Update Image</label>

                    <input 
                        type="file" 
                        class="form-control-filejustify-content-center" v-on:change="onFileChange" 
                        id="image" 
                        ref="image"
                        style="display: flex; flex-direction: column; align-items: center;" />

                    <div v-if="errors.image" class="text-danger">{{ errors.image }}</div>
                </div>

                <!-- <br> -->

                <div class="form-group d-flex justify-content-center">
                    <button type="submit" class="btn btn-outline-primary">Update Post</button>

                    <router-link to="/feed" class="btn btn-outline-secondary ml-2" style="margin-left: 10px;">Cancel</router-link>
                </div>

                
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import refreshAccessToken from '@/utils/refresh_token.js';

export default {
    name: 'UpdatePostView',
    data() {
        return {
            post: {
                title: '',
                caption: ''
            },
            errors: {},
            image: null
        }
    },

    created() {
        this.fetchPostData()
    },

    methods: {
        async fetchPostData() {
            const post_id = this.$route.params.post_id

            try {
                let access_token = localStorage.getItem('access_token')
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                // Send a GET request to the server to fetch the post data
                const response = await axios.get(`http://127.0.0.1:5000/api/post/${post_id}`)

                this.post = response.data

            } catch (error) {
                if (error.response.status === 401) {
                    await refreshAccessToken()
                    await this.fetchPostData()
                }

                else {
                    console.error(error)
                    alert('An error occurred while fetching the post data.')
                }
            }
        },

        async updatePost() {

            this.errors = {}
            let formData = new FormData()

            // Append the post data to the FormData object
            formData.append('data', JSON.stringify(this.post))

            // Append the image file to the FormData object (if provided)
            if (this.image) {
                formData.append('image', this.image)
            }

            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                const post_id = this.$route.params.post_id

                await axios.put(`http://127.0.0.1:5000/api/post/${post_id}`, formData)

                this.$router.push(`/feed`)

            } catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken()
                    await this.updatePost()
                }

                // handle validation errors.
                else if (error.response && error.response.status === 400 || error.response.status === 422) {
                    this.errors = error.response.data.errors
                    alert('An error occurred while updating the post.')
                }
            }
        },

        onFileChange(event) {
            // Get the selected file from the input element
            this.image = event.target.files[0]
        }
    }
}
</script>


<style>

</style>
