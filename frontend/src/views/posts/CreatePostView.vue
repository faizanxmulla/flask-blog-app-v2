<template>
    <div class="container d-flex justify-content-center">
        <div class="col-lg-6 col-md-8 col-sm-10" style="margin-top:20px">
            <h5 class="text-center">Create a new post</h5>
            <p class="text-center">Fill the form to create a new post.</p>
            <hr>
            <br>

            <form @submit.prevent="createPost()" enctype="multipart/form-data">

                <div class="form-group" style="display: flex; flex-direction: column; align-items: center;">

                    <label for="post.title">Title</label>

                    <input 
                        type="text" 
                        class="form-control" 
                        v-model="post.title" 
                        placeholder="Enter title" style="width:80%; margin-top:7px">

                    <div v-if="errors.title" class="text-danger">{{ errors.title }}</div>

                </div>

                <br>

                <div class="form-group" style="display: flex; flex-direction: column; align-items: center;">

                    <label for="post.caption">Caption</label>

                    <textarea 
                        class="form-control" 
                        v-model="post.caption" placeholder="Enter Caption / Description" 
                        style="width:80%; margin-top:7px" rows="6">
                    </textarea>

                    <div v-if="errors.caption" class="text-danger">{{ errors.caption }}</div>
                </div>


                <!-- Handling SAFE HTML tags (doesn't work)-->
                <!-- <div class="form-group" style="display: flex; flex-direction: column; align-items: center;">


                    <label for="post.caption">Caption</label>

                    <div style="width:80%; margin-top:7px">
                        <span v-html="post.caption"></span>

                        <textarea
                            class="form-control"
                            v-model="post.caption"
                            @input="removeHTMLtags"
                            placeholder="Enter Caption / Description"
                            rows="6">
                        </textarea>
                    </div>


                    <div v-if="errors.caption" class="text-danger">{{ errors.caption }}</div>
                </div> -->
                
                <br>

                <div class="form-group" style="display: flex; flex-direction: column; align-items: center;">

                    <label for="image">Post Image </label>

                    <input 
                        type="file" 
                        class="form-control-filejustify-content-center" v-on:change="onFileChange" 
                        id="image" 
                        ref="image"
                        style="display: block; flex-direction: column; align-items: center;">

                    <div v-if="errors.image" class="text-danger">{{ errors.image }}</div>

                </div>

                <div class="form-group d-flex justify-content-center">
                    <button 
                        type="submit" 
                        class="btn btn-outline-primary" style="align-items: center;">Create Post
                    </button>
                </div>
                
                
            </form>
        </div>
    </div>
</template>


<script>
import axios from 'axios'
import refreshAccessToken from '@/utils/refresh_token.js';

export default {
    name: 'CreatePostView',
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
    methods: {
        async createPost() {
            // Reset the errors object
            this.errors = {}

            // Create a new FormData object
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

                await axios.post('http://127.0.0.1:5000/api/post', formData)

                this.$router.push('/feed')

            } catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken()
                    await this.createPost()
                }

                else if (error.response &&  error.response.status === 400 || error.response &&  error.response.status === 422) {
                    this.errors = error.response.data.errors
                    alert('An error occurred while creating the post.')
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


<style></style>