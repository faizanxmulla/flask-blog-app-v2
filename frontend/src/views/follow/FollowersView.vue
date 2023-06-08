<template>
    <div class="container mt-2">
        <div class="container d-flex justify-content-center">
            <div class="col-lg-6 col-md-8 col-sm-10" style="margin-top: 50px">

                <h5 class="text-center">Followers page :</h5>

                <p class="text-center">It consists of the list of usernames who are following you.</p>

                <hr>

                <table class="text-center d-flex justify-content-center">

                    <tbody style="display: block; flex-wrap: nowrap; justify-content: center; align-items: center;">

                        <tr v-for="follower in followers" :key="follower.id" class="d-flex justify-content-center align-items-center">
                            
                            <td class="text-center" style="font-size: 20px">

                                <a :href="`/profile/${follower.username}`">{{ follower.username }} </a>
                                
                            </td>

                            <td>
                                <div class=" follow-unfollow-btn-container ml-3">

                                    <button v-if="follower.followed" @click="unfollowUser(follower.username)" class="btn btn-outline-danger ">Unfollow</button>

                                    <button v-else @click="followUser(follower.username)" class="btn btn-outline-success">Follow</button>
                                </div>
                                
                            </td>

                        </tr>
                    </tbody>
                </table>

                <br>
                <br>

                <p v-if="!followers.length" class="text-center" style="font-size : 18px;"><i> Looks like you don't have any followers yet !! </i></p>

            </div>
        </div>
    </div>
</template>


<script>
import axios from 'axios'
import refreshAccessToken from '@/utils/refresh_token.js'

export default {
    name: 'FollowersView',
    data() {
        return {
            followers: []
        }
    },

    created() {
        console.log('created hook called');
        // fetch the followers data for the logged in user.
        this.fetchFollowersData(this.$route.params.username)
    },

    methods: {
        async fetchFollowersData(username) {
            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                // list of followers of the logged-in user.
                const followersResponse = await axios.get(`http://127.0.0.1:5000/api/followers/${username}`)

                const followers = followersResponse.data.followers

                // list of users that the logged-in user is already following.
                const followingResponse = await axios.get(`http://127.0.0.1:5000/api/following/${username}`)

                const following = followingResponse.data.following

                console.log('followers:', followers);
                console.log('following:', following);

                // Set the `followed` property of each follower in the `followers` array based on whether or not the logged-in user is already following them.

                if (followers.length > 0 && following.length > 0) {
                    followers.forEach((follower) => {
                        follower.followed = following.some((user) => user.username === follower.username)
                    })
                } else {
                    console.error('Empty followers or following array')
                }
                
                console.log('followers after setting followed:', followers);
                this.followers = followers

            } catch (error) {

                if (error.response && error.response.status === 401) {
                    await refreshAccessToken()
                    await this.fetchFollowersData(username)
                }

                else if (error.response) {
                    console.error(error)
                    alert('An error occurred while fetching the followers data.')
                }
            }
        },

        async followUser(username) {
            try {
                let access_token = localStorage.getItem('access_token')

                console.log(`followUser called for ${username}`);
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                await axios.post(`http://127.0.0.1:5000/api/follow/${username}`)

                const index = this.followers.findIndex((follower) => follower.username === username)

                console.log(`index of ${username} in followers:`, index);

                if (index !== -1) {
                    this.followers[index].followed = true
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
                let access_token = localStorage.getItem('access_token')

                console.log(`unfollowUser called for ${username}`);

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                await axios.post(`http://127.0.0.1:5000/api/unfollow/${username}`)

                const index = this.followers.findIndex((follower) => follower.username === username)

                console.log(`index of ${username} in followers:`, index);

                if (index !== -1) {
                    this.followers[index].followed = false
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
