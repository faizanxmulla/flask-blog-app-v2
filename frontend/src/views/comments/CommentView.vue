<template>
    <div class="d-flex flex-column">

        <div class="d-flex justify-content-center">

            <div class="existing-comments">

                <div v-if="existing_comments.length > 0">

                    <div class="card card-inner mb-2" v-for="comment in existing_comments" :key="comment.id">

                        <div class="card-header d-flex justify-content-between align-items-center">

                            <a :href="`/profile/${comment.username}`">
                                <h5>{{ comment.username }}</h5>
                            </a>

                            <small class="text-muted" v-if="comment.last_edited">Last edited on :
                                {{
                                    new Date(comment.last_edited).toLocaleString("en-US", {
                                        timeZone: "Asia/Kolkata",
                                    })
                                }}</small>

                            <small class="text-muted" v-else>Commented on :
                                {{
                                    new Date(comment.timestamp).toLocaleString("en-US", {
                                        timeZone: "Asia/Kolkata",
                                    })
                                }}</small>

                        </div>

                        <div class="card-body">
                            <p>{{ comment.content }}</p>
                        </div>

                        <div class="comment-actions">

                            <div v-if="comment.is_current_user" class="card-footer d-flex justify-content-end">

                                <a :href="`/post/${comment.post_id}/comment/${comment.id}/update`"
                                    class="btn btn-outline-primary btn-sm">Update</a>

                                <a :href="`/post/${comment.post_id}/comment/${comment.id}/delete`"
                                    class="btn btn-outline-danger btn-sm ml-2">Delete</a>

                            </div>
                        </div>
                    </div>
                </div>

                <div v-else>
                    <p class="text-center" style="font-size : 22px; margin-top:5%"><i>No Comments yet !!</i></p>
                </div>


            </div>
        </div>


        <div class="add-comment-form-sticky-bottom ">
            <hr>

            <form @submit.prevent="createComment()">

                <div class="form-group d-flex justify-content-center">

                    <textarea class="form-control" v-model="comment.content" placeholder="Add new comment ...."
                        style="width:60%;margin-top:7px" rows="3">
                            </textarea>

                    <div v-if="errors.content" class="text-danger">{{ errors.content }}</div>

                </div>

                <div class="form-group d-flex justify-content-center">

                    <br>
                    <button type="submit" class="btn btn-outline-primary">Add Comment</button>

                </div>

            </form>
        </div>
    </div>
</template>




<script>
import axios from 'axios'
import refreshAccessToken from '@/utils/refresh_token.js';

export default {
    name: 'CommentView',
    data() {
        return {
            comment: {
                content: ''
            },

            errors: {},
            existing_comments: [],
            is_current_user: false
        }
    },

    methods: {
        async createComment() {
            this.errors = {}

            // get the post on which we want to comment.
            const post_id = this.$route.params.post_id

            let formData = new FormData();

            formData.append('data', JSON.stringify(this.comment))

            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                const response = await axios.post(`http://127.0.0.1:5000/api/post/${post_id}/comment`, formData)

                // add the newly created comment to the existing_comments array.
                this.existing_comments.push(response.data.data)

                // Reset the comment object to clear the textarea
                this.comment.content = ''

                this.loadExistingComments()

            } catch (error) {

                if (error.response && error.response.status === 401) {
                    await refreshAccessToken()
                    await this.createComment()
                }

                else if (error.response.status === 400 || error.response.status === 422) {
                    this.errors = error.response.data.errors
                    alert('An error occurred while commenthin on this post.')
                }
            }
        },

        async loadExistingComments() {
            const post_id = this.$route.params.post_id

            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                const response = await axios.get(`http://127.0.0.1:5000/api/post/${post_id}/comment`);

                // loop through each comment in the response data. [did this because on adding new comment username and timestamp were not showing unless page is refreshed]

                // response.data.data.forEach(comment => {
                //     // add the comment username and timestamp to the comment object.
                //     comment.username = comment.user.username;
                //     comment.timestamp = new Date(comment.timestamp).toLocaleString("en-US", {
                //         timeZone: "Asia/Kolkata"});
                // });

                this.existing_comments = response.data.data;
            }

            catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken()
                    await this.loadExistingComments()
                }

                else {
                    console.error(error)
                    alert('An error occurred while fetching the comment data.')
                }
            }
        },
    },

    mounted() {
        this.loadExistingComments();
    },
}
</script>


<style>
.add-comment-form-sticky-bottom {
    position: fixed;
    bottom: 5px;
    left: 220px;
    right: 50px;
    width: 70%;
}

.existing-comments {
    overflow: auto;
    max-height: 60vh;
    width: 70%
}

.d-flex.justify-content-center {
    margin-top: 20px;
}
</style>