<template>
    <div class="container d-flex justify-content-center mt-5">
        <div class="col-lg-6 col-md-8 col-sm-10">

            <h4 class="text-center">Feed Page</h4>
            <p class="text-center">Welcome to your feed !! <br>Enjoy the latest updates from your network.</p>
            <hr>
            <br>

            <div v-if="posts.length === 0">
                <br>
                <br>

                <p class="text-center" style="font-size : 20px">
                    <i>There are no posts in your feed. <br> Connect with other users to see what they are posting.</i>
                </p>
            </div>

            <div v-for="post in posts" :key="post.id" class="card card-inner mb-2" style="width:100%">

                <div class="card-header d-flex justify-content-between align-items-center">

                    <router-link :to="{ name: 'Profile-Page', params: { username: post.username } }">
                        <h5>{{ post.username }}</h5>
                    </router-link>

                    <small class="text-muted" v-if="post.last_updated">Last updated on : {{ formatTimestamp(post.last_updated) }}</small>

                        <small class="text-muted" v-else>Created on : {{ formatTimestamp(post.timestamp) }}</small>
                </div>

                <div class="card-body" style="display: flex; flex-direction: column">

                    <h5 class="card-title">{{ post.title }}</h5>
                    <br>

                    <img 
                        v-if="post.post_image_url" 
                        :src="post.post_image_url" 
                        :alt="post.title"
                        class="card-img-top" 
                        style="width: auto; height: 300px; object-fit: cover;">
                    <br>


                    <p class="card-text" style="font-size:17px"> <strong>Caption :</strong>
                        {{ post.caption }}</p>

                
                </div>

                <div class="card-footer">
                    <a :href="'/post/' + post.id + '/comment'" class="btn btn-outline-info"> Comments : {{ post.comments_count }}
                    </a>
                </div>

            </div>

            <div v-if="posts.feed_post_count === 0">
                <br>
                <br>
                <p class="text-center" style="font-size : 20px; margin-top:5%"><i>There are no posts in your feed. <br> Connect with other users to see what they are posting.</i></p>
            </div>

        </div>
        
    </div>
</template>


<script>
import axios from 'axios';
import refreshAccessToken from '@/utils/refresh_token.js';


export default {
    name: 'FeedView',
    data() {
        return {
            posts: [],
        }
    },

    created() {
        this.fetchFeedData();
    },

    methods: {
        async fetchFeedData() {
            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                const response = await axios.get(`http://127.0.0.1:5000/api/feed`)

                this.posts = response.data.data;
            }

            catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken()
                    await this.fetchFeedData()
                }
                else {
                    console.log(error)
                }
            }
        },

        formatTimestamp(timestamp) {
            const date = new Date(timestamp);
            return date.toLocaleString('en-US', { timeZone: 'Asia/Kolkata' });
        },

    },
};
</script>
