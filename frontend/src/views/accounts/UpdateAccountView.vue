<template>
    <div class="container d-flex justify-content-center ">
        <div class="col-lg-6 col-md-8 col-sm-10" style="margin-top: 30px;">
            <h4 class="text-center">Update Account</h4>
            <p class="text-center">Fill the details to update account information.</p>
            <hr>
            <br>

            <form @submit.prevent="updateAccount()" enctype="multipart/form-data">

                <div class="form-group" style="display: flex; flex-direction: column; align-items: center;">
                    <label for="account.username">Username : </label>

                    <input 
                        v-model="account.username" 
                        type="text" 
                        class="form-control" 
                        placeholder="Enter username"
                        style="width:50%; margin-top:5px;" />

                    <div v-if="errors.username" class="text-danger">{{ errors.username }}</div>

                </div>

                <br>

                <div class="form-group" style="display: flex; flex-direction: column; align-items: center;">

                    <label for="account.email">Email : </label>

                    <input 
                        v-model="account.email" 
                        type="text" 
                        class="form-control" 
                        placeholder="Enter email address"
                        style="width:50%; margin-top:5px;" />

                    <div v-if="errors.email" class="text-danger">{{ errors.email }}</div>

                </div>

                <br>

                <div class="form-group" style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
                    <label for="profile_image">Profile Image : </label>

                    <input 
                        type="file" 
                        class="form-control-filejustify-content-center" 
                        v-on:change="onFileChange"
                        id="profile_image"
                        ref="profile_image"
                        style="margin-left: 10px;" />

                    <div v-if="errors.profile_image" class="text-danger">{{ errors.profile_image }}</div>

                </div>

                <br>

                <div class="form-group d-flex justify-content-center" >
                    <button type="submit" class="btn btn-outline-primary">Update Account
                    </button>

                    <router-link :to="{ path: '/profile/' + account.username}" class="btn btn-outline-secondary ml-2"
                        style="margin-left: 10px;">Cancel</router-link>
                </div>
            </form>
        </div>
    </div>
</template>



<script>
import axios from 'axios';
import refreshAccessToken from '@/utils/refresh_token.js';

export default {
    name: 'UpdateAccountView',
    data() {
        return {
            account: {
                username: '',
                email: '',
            },
            profile_image: null,
            errors: {},
        };
    },

    methods: {
        async fetchUserData() {
            try {
                let access_token = localStorage.getItem('access_token');

                axios.defaults.headers.common['Authorization'] = 'Bearer' + access_token

                const response = await axios.get('http://127.0.0.1:5000/api/user');

                this.account = response.data
                
            } catch (error) {
                if (error.response.status === 401) {
                    await refreshAccessToken();
                    await this.fetchUserData();
                } 
                
                else {
                    console.error(error);
                    alert('An error occurred while fetching the user data.');
                }
            }
        },

        async updateAccount() {
            this.errors = {}

            let formData = new FormData();

            formData.append('data', JSON.stringify(this.account))

            if (this.profile_image) {
                formData.append('profile_image', this.profile_image);
            }

            try {
                let access_token = localStorage.getItem('access_token');

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;

                await axios.put('http://127.0.0.1:5000/api/user', formData);

                this.$router.push(`/profile/${this.account.username}`);

            } catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken();
                    await this.updateAccount();
                } 
                
                else if (error.response && error.response.status === 400 || error.response.status === 422) {
                    this.errors = error.response.data.errors;
                    alert('An error occurred while updating the account.')
                } 
            }
        },

        onFileChange(event) {
            if (event.target.files.length > 0) {
                this.profile_image = event.target.files[0];
            }
        },
    },
};
</script>
