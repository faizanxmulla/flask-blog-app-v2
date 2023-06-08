<template>
    <div class="container mt-2">
        
        <div class="container d-flex justify-content-center">

            <div class="col-lg-6 col-md-8 col-sm-10" style="margin-top: 50px">

                <h5 class="text-center">Following page :</h5>

                <p class="text-center">It consists of the list of usernames whom you are following.</p>

                <hr>

                <table class="text-center d-flex justify-content-center">

                    <tbody style="display: block; flex-wrap: nowrap; justify-content: center; align-items: center;">

                        <tr v-for="user in following" :key="user.id" class="d-flex justify-content-center">

                            <td class="text-center" style="font-size: 20px">
                            
                                <a :href="`/profile/${user.username}`">{{ user.username }}</a>
                            
                            </td>

                            <td>
                                <div class=" follow-unfollow-btn-container ml-3">

                                    <button  v-if="user.followed" @click="unfollowUser(user.username)" class="btn btn-outline-danger">Unfollow</button>

                                    <button v-else @click="followUser(user.username)" class="btn btn-outline-success">Follow</button>
                                </div>
                        
                            </td>
                        </tr>
                    </tbody>
                </table>

                <br>
                <br>

                <p v-if="!following.length" class="text-center" style="font-size : 18px;"> <i> Looks like you haven't started following anyone yet !! </i> </p>

            </div>
        </div>
    </div>
</template>



<script>

import axios from 'axios'
import refreshAccessToken from '@/utils/refresh_token.js'

export default {
    name: 'FollowingView',
    data() {
        return {
            following: []
        }
    },

    created() {
        console.log('created hook called');
        // Fetch the following data for the logged in user.
        this.fetchFollowingData(this.$route.params.username)
    },

    methods: {
        async fetchFollowingData(username) {
            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                // Get the list of users that the logged-in user is already following
                const followingResponse = await axios.get(`http://127.0.0.1:5000/api/following/${username}`)

                const following = followingResponse.data.following

                console.log('following:', following);

                // set the 'followed' property of each user in the following array based on whether or not the logged in user is already following them.

                if (following.length > 0){
                    following.forEach((user) => {
                        user.followed = true
                    })
                } else {
                    console.error('Empty following array')
                }
                
                this.following = following

            } catch (error) {

                if (error.response && error.response.status === 401) {
                    await refreshAccessToken()
                    await this.fetchFollowingData(username)
                }

                else if (error.response) {
                    console.error(error)
                    alert('An error occurred while fetching the following data.')
                }
            }
        },

        async followUser(username) {
            try {
                let access_token = localStorage.getItem('access_token')

                console.log(`followUser called for ${username}`);
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                await axios.post(`http://127.0.0.1:5000/api/follow/${username}`)

                const index = this.following.findIndex((user) => user.username === username)

                console.log(`index of ${username} in followers:`, index);

                if (index !== -1) {
                    this.following[index].followed = true
                }

            } catch (error) {

                if (error.response.status === 401) {
                    await refreshAccessToken()
                    await this.followUser(username)
                }

                else {
                    console.error(error)
                    alert('An error occurred while following the user.')
                }
            }
        },


        async unfollowUser(username) {
            try {
                let access_token = localStorage.getItem
                ('access_token')

                console.log(`unfollowUser called for ${username}`);

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                await axios.post(`http://127.0.0.1:5000/api/unfollow/${username}`)

                const index = this.following.findIndex((user) => user.username === username)

                console.log(`index of ${username} in followers:`, index);

                if (index !== -1) {
                    this.following[index].followed = false
                }

            } catch (error) {

                if (error.response.status === 401) {
                    await refreshAccessToken()
                    await this.unfollowUser(username)
                }

                else {
                    console.error(error)
                    alert('An error occurred while unfollowing the user.')
                }
            }
        },

        
    }
}
</script>