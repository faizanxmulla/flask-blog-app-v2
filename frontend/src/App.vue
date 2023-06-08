<template>
    <div id="app">

        <div v-if="shouldShowNavBar">
            <NavBar 
            :currentUser="currentUser" :showDropdown="showDropdown" @toggleDropdown="toggleDropdown"/>
        </div>

        <router-view :currentUser="currentUser" :post_id="post_id" :comment_id="comment_id" :username="username"/>

    </div>
</template>


<script>
import axios from "axios";
import NavBar from "../src/components/Navbar.vue"

export default {
    name: 'App',
    components: {
        NavBar,
    },
    
    data() {
        return {
            currentUser: {},
            routeswithoutNavbar: ['/', '/register', '/login'],
            showDropdown: false,
            username: null,
            password: "",
            post_id: null,
            comment_id: null,
        };
    },

    created() {
        // Get post_id and comment_id from the URL params
        this.post_id = this.$route.params.post_id;
        this.comment_id = this.$route.params.comment_id;
        this.username = this.$route.params.username;
    },


    methods: {
        async login() {
            const response = await axios.post('http://127.0.0.1:5000/api/login', {username: this.username, password: this.password});

            const userData = response.data;

            this.currentUser = {
                username: userData.username,
            }
        },

        toggleDropdown() {
            this.showDropdown = !this.showDropdown;
        },
    },

    computed: {
        shouldShowNavBar() {
            return !['/', '/register', '/login'].includes(this.$route.path)
        }, 
    }
};
</script>


<style>

</style>
