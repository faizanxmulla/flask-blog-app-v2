<template>
    <div>
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <a class="navbar-brand" href="#">Flask Blog App - v2.0</a>
            
            <button 
                class="navbar-toggler" 
                type="button" 
                data-toggle="collapse" 
                data-target="#navbarNav"
                aria-controls="navbarNav" 
                aria-expanded="false" 
                aria-label="Toggle navigation"
                @click="$emit('toggleDropdown')">
                

                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" :class="{ 'show': showDropdown }" id="navbarNav">

                <ul class="navbar-nav ml-auto">

                    <li class="nav-item mr-5">
                        <a class="nav-link" style="font-size:large" > <b>Username :</b> {{ profile.username }}</a>
                    </li>


                    <template>
                        <li class="nav-item">
                            <router-link class="nav-link" to="/feed">Feed</router-link>
                        </li>

                        <li class="nav-item">
                            <router-link class="nav-link" to="/search">Search</router-link>
                        </li>

                        <li class="nav-item">
                            <router-link :to="{ name: 'Profile-Page', params: { username: profile.username } }" class="nav-link">Profile</router-link>
                        </li>

                        <li class="nav-item">
                            <router-link class="nav-link" to="/create-post">Create Post</router-link>
                        </li>

                        <li class="nav-item">
                            <a class="nav-link" @click="logoutUser()">Logout</a>
                        </li>

                    </template>

                </ul>
            </div>
        </nav>
    </div>
    
</template>


<script>

import axios from "axios";
import refreshAccessToken from '@/utils/refresh_token.js';

export default {
    name: 'NavBar',

    data() {
        return {
            profile: {
                username: '',
            },

            is_current_user: false,
        }
    },  

    props: {
        showDropdown: {
            type: Boolean,
            required: true
        }
    },
    
    methods: {
        async getUserData(username) {
            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                const response = await axios.get(`http://127.0.0.1:5000/api/profile/${username}`)

                this.profile = response.data.data;
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

        async logoutUser() {
            try {
                localStorage.removeItem('access_token')
                localStorage.removeItem('refresh_token')
                localStorage.removeItem('username')

                alert('Successfully logged out !!')
                this.$router.push('/login')
            } 

            catch (error){
                console.log(error)
            }
            
        }
    },

    created() {
        const username = localStorage.getItem('username')
        this.getUserData(username)
    },

    mounted() {

        // console.log('route params:', this.$route.params)
        // const username = this.$route.params.username;
        // console.log('username:', username)
        // this.getUserData(username);


        const script = document.createElement('script')
        script.src = 'https://code.jquery.com/jquery-3.5.1.slim.min.js'
        script.integrity = 'sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj'
        script.crossOrigin = 'anonymous'
        document.head.appendChild(script)
    
        const bootstrap = document.createElement('script')
        bootstrap.src = 'https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js'
        bootstrap.integrity = 'sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV'
        bootstrap.crossOrigin = 'anonymous'
        document.head.appendChild(bootstrap)
    }
};
</script>


