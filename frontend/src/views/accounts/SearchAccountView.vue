<template>
    <div class="container d-flex justify-content-center mt-5">
        <div class="col-lg-6 col-md-8 col-sm-10" style="margin-top: 50px;">
            <h4 class="text-center">Search Page</h4>
            <p class="text-center">Use the search box to search other users using their usernames.</p>
            <hr>
            <br>

            <form @submit.prevent="searchUsers">

                <div class="form-group d-flex justify-content-center">
                    <input v-model="query" class="form-control" placeholder="Type a username ..." style="width:70%">
                </div>

                <div class="form-group d-flex justify-content-center">
                    <button type="submit" class="btn btn-outline-primary">Search</button>
                </div>
            </form>

            <div class="d-flex justify-content-center mt-3" v-if="users.length > 0">
                <ul v-for="user in users" :key="user.id" style="margin-down: 10px;">
                    <a :href="`/profile/${user.username}`">{{ user.username }}</a>
                </ul>
            </div>

            <br>

            <div class="d-flex justify-content-center" v-if="users.length === 0 && query !== ''">
                <p>No results found for "{{ query }}."</p>
            </div>
        </div>
        
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'SearchAccountView',
    data() {
        return {
            query: '',
            users: [],
            errors: {},
        };
    },

    methods: {
        async searchUsers() {
            this.users = [];
            this.errors = {};

            if (!this.query) {
                this.errors.query = 'Please enter a query !!.';
                return;
            }

            try {
                const response = await axios.get(`http://127.0.0.1:5000/api/user?query=${this.query}`, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
                    },
                });
                this.users = response.data.data;

            } 
            
            catch (err) {
                if (err.response.status === 401) {
                    this.$router.push('/login');
                    return;
                }

                if (err.response.status === 400) {
                    this.errors.query = 'Please enter a valid search term.';
                    return;
                }

                this.errors.query = 'An error occurred while searching for users.';
            }
        },
    },

    // using watch property to watch changes in the query data property and trigger searchUsers() method whenever query changes. 
    watch: {
        query: function() {
            this.searchUsers();
        }
    }

};
</script>
