<template>
    <div class="container d-flex justify-content-center ">
        <div class="col-lg-6 col-md-8 col-sm-10" style="margin-top:40px">
            <h4 class="text-center">Delete Account</h4>
            <p class="text-center">Are you sure you want to delete your account ?? <br> This action cannot be <b>undone</b>.</p>
            <hr>
            <br>

            <form @submit.prevent="deleteAccount()">

                <div class="form-group" style="display: flex; flex-direction: column; align-items: center;">
                    <label for="account.password">Password</label>

                    <input 
                        type="password" 
                        id="password" 
                        v-model="account.password" class="form-control" 
                        style="width:300px"
                        placeholder="Enter Password">

                    <div v-if="errors.password" class="text-danger">{{ errors.password }}</div>

                </div>

                <br>

                <div class="form-group" style="display: flex; flex-direction: column; align-items: center;">

                    <label for="confirm-password">Confirm Password</label>

                    <input 
                        type="password" 
                        id="confirm-password" v-model="account.confirmPassword" class="form-control"
                        style="width:300px" 
                        placeholder="Confirm Password">

                    <div v-if="errors.confirmPassword" class="text-danger">{{ errors.confirmPassword }}</div>

                </div>

                <br>

                <div class="d-flex justify-content-center">
                    <input 
                        type="submit" 
                        value="Delete Account" 
                        class="btn btn-outline-danger">

                    <router-link :to="'/feed' + account.username" class="btn btn-outline-secondary" style="margin-left: 10px;">Cancel</router-link>
                </div>

                
            </form>

        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'DeleteAccountView',
    data() {
        return {
            account: {
                username: '',
                password: '',
                confirmPassword: '',

            },
            errors: {},
        };
    },

    methods: {
        async deleteAccount() {
            // Perform validation before sending the request
            this.errors = {};
            if (!this.account.password) {
                this.errors.password = 'Please enter your password.';
            }
            if (!this.account.confirmPassword) {
                this.errors.confirmPassword = 'Please confirm your password.';
            }
            if (this.account.password !== this.account.confirmPassword) {
                this.errors.confirmPassword = 'Passwords do not match.';
            }

            if (Object.keys(this.errors).length) {
                return;
            }

            try {
                await axios.delete('http://127.0.0.1:5000/api/user', {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
                    },
                    data: {
                        password: this.account.password,
                    },
                });

                localStorage.removeItem('user');
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token')

                alert('Account deleted successfully !!')
                this.$router.push('/login');

            }

            catch (err) {
                // Handle error response
                if (err.response.status === 401) {
                    this.$router.push('/login');
                    return;
                }
                if (err.response.status === 403) {
                    this.errors.password = 'You are not authorized to delete this account.';
                    return;
                }
                if (err.response.status === 404) {
                    this.errors.password = 'User not found.';
                    return;
                }
                this.errors.password = 'Incorrect password.';
            }

        }
    }
}
</script>
