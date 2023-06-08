<template>
    <div class="container mt-5">
        <div class="row">

            <div class="col-md-4">
                <img v-if="profile.profile_image_url" 
                    :src="profile.profile_image_url" 
                    class="img-fluid rounded-circle" 
                    style="object-fit: cover; margin-top: 35px;">
            </div>

            <div class="col-md-8">

                <div class="d-flex justify-content-between align-items-center mt-4">
                    <h4>{{ profile.username }}</h4>
                </div>

                <div class="d-flex justify-content-between align-items-center">
                    <p class="text-muted">{{ profile.email }}</p>
                    <br />
                </div>

                <div v-if="!profile.is_current_user" class="profile-action mt-3">

                    <button :class="[is_following ? 'btn btn-outline-danger' : 'btn btn-outline-success']"
                        @click="followOrUnfollowUser(profile.username)">
                        {{ is_following ? "Unfollow" : "Follow" }}
                    </button>
                </div>

                <div v-else class="profile-action">
                    <a href="/update-account" class="btn btn-outline-primary ml-auto">Update</a>
                    <a href="/delete-account" class="btn btn-outline-danger ml-2 ">Delete</a>

                    <button class="btn btn-outline-info ml-2" @click="exportPostsCSV()">Export</button>
                </div>

                <br />

                <p style="font-size: 20px">Total posts: {{ profile.total_posts }}</p>

                <p style="font-size: 20px"><a :href="'/followers/' + profile.username">Followers: {{
                    profile.followers_count }}</a></p>

                <p style="font-size: 20px"><a :href="'/following/' + profile.username">Following: {{
                    profile.following_count }}</a></p>

            </div>

            <div v-if="is_following || profile.is_current_user">

                <div class="card card-body bg-light mt-5">
                    <h4>My Posts</h4>

                    <div v-if="profile.posts.length > 0">

                        <div v-for="post in profile.posts" :key="post.id">

                            <div class="card card-inner mb-2">

                                <div class="card-header d-flex justify-content-between align-items-center">

                                    <h6>{{ post.title }}</h6>

                                    <small class="text-muted" v-if="post.last_updated">Last updated on :
                                        {{
                                            new Date(post.last_updated).toLocaleString("en-US", {
                                                timeZone: "Asia/Kolkata",
                                            })
                                        }}</small>

                                    <small class="text-muted" v-else>Created on :
                                        {{
                                            new Date(post.timestamp).toLocaleString("en-US", {
                                                timeZone: "Asia/Kolkata",
                                            })
                                        }}</small>

                                </div>

                                <div class="card-body">
                                    <img v-if="post.post_image_url" 
                                        :src="post.post_image_url"
                                        class="img-fluid rounded post-image"
                                        width="500" 
                                        height="300">

                                    <br />
                                    <br />

                                    <p><strong>Caption : </strong>{{ post.caption }}</p>

                                </div>

                                <div class="card-footer d-flex justify-content-between">

                                    <a :href="'/post/' + post.id + '/comment'" class="btn btn-outline-info">Comments : {{
                                        post.comments_count }}</a>

                                    <div class="btn-group" v-if="profile.is_current_user">

                                        <a :href="'/post/' + post.id + '/update'"
                                            class="btn btn-outline-primary ">Update</a>

                                        <a :href="'/post/' + post.id + '/delete'"
                                            class="btn btn-outline-danger ml-2">Delete</a>

                                    </div>

                                </div>

                            </div>
                        </div>
                    </div>
                </div>
            </div>


            <div v-else class="d-flex flex-column justify-content-center align-items-center mt-5">
                <img src="https://cdn2.iconfinder.com/data/icons/billing-shipping/100/Account_Locked-512.png"
                    alt="Private Account" width="50" height="50">

                <br>

                <p style="font-size: 20px"><b>This account is private.</b></p>
                <p style="font-size: 17px">Follow this account to see their photos.</p>
            </div>

        </div>
    </div>
</template>


<script>

import axios from "axios";
import refreshAccessToken from '@/utils/refresh_token.js';

export default {
    name: 'ProfileView',

    data() {
        return {
            profile: {
                id: '',
                username: '',
                email: '',
                profile_image: '',
                profile_image_url: '',
                posts: [],
                total_posts: 0,
                followers_count: 0,
                following_count: 0,
                comments_count: 0,
            },

            is_following: null,
            is_current_user: false,
        };
    },

    created() {
        this.getUserData(this.$route.params.username);
        const is_following = localStorage.getItem('is_following');

        if (is_following !== null) {
            this.is_following = JSON.parse(is_following);
        }
    },

    methods: {
        async getUserData(username) {
            try {
                let access_token = localStorage.getItem('access_token')
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                const response = await axios.get(`http://127.0.0.1:5000/api/profile/${username}`)

                this.profile = response.data.data;
                this.is_following = response.data.is_following;
                this.is_current_user = response.data.is_current_user;

            }

            catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken()
                    await this.getUserData(username)
                }
                else {
                    console.log(error)
                }
            }
        },

        async followOrUnfollowUser(username) {
            console.log('is_following before:', this.is_following);

            if (this.is_following === null) {
                await this.getUserData(username);
            }

            if (this.is_following) {
                await this.unfollowUser(username)
                this.is_following = false;
            }

            else {
                await this.followUser(username)
                this.is_following = true;
            }

            console.log('is_following after:', this.is_following);
            localStorage.setItem('is_following', this.is_following);
        },


        async followUser(username) {
            try {
                let access_token = localStorage.getItem('access_token')
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                await axios.post(`http://127.0.0.1:5000/api/follow/${username}`)

                this.is_following = true
                this.profile.followers_count += 1;

                localStorage.setItem('is_following', 'true');

            } catch (error) {
                if (error.response.status === 401) {
                    await refreshAccessToken()
                    await this.followUser(username)
                } else {
                    console.error(error)
                    alert('An error occurred while following the user.')
                }
            }
        },

        async unfollowUser(username) {
            try {
                let access_token = localStorage.getItem('access_token')
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                await axios.post(`http://127.0.0.1:5000/api/unfollow/${username}`)

                this.is_following = false
                this.profile.followers_count -= 1;

                localStorage.setItem('is_following', 'false');

            } catch (error) {
                if (error.response.status === 401) {
                    await refreshAccessToken()
                    await this.unfollowUser(username)
                } else {
                    console.error(error)
                    alert('An error occurred while unfollowing the user.')
                }
            }
        },

        async exportPostsCSV() {
            try {
                let access_token = localStorage.getItem('access_token')
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                const response = await axios.get(`http://127.0.0.1:5000/api/export-posts-csv`, { responseType: 'arraybuffer' })

                const url = window.URL.createObjectURL(new Blob([response.data]))
                const link = document.createElement('a')

                // setting filenames.
                const now = new Date().toLocaleString().replace(/[^\w\s]/gi, '').replace(/ /g, '_')
                const post_filename = `posts_${now}.csv`

                link.href = url
                link.setAttribute('download', post_filename)
                document.body.appendChild(link)
                link.click()

                // code to : Save the file to a custom location.
                // const fileSaver = new FileSaver(url);
                // fileSaver.save(post_filename, {
                //     type: 'text/csv',
                // });


            } catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken()
                    await this.exportPostsCSV()
                } else {
                    console.error(error)
                    alert('An error occurred while exporting CSV files.')
                }
            }
        },

    },

};

</script>

<style>
.post-image {
    max-width: auto;
    height: auto;
}
</style>

