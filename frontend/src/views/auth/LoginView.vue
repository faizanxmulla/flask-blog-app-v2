<template>
<div>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand" href="#">Flask Blog App - v2.0 </a>
    <button
        class="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ml-auto">
        <li class="nav-item">
            <a class="nav-link" href="/">Home</a>
        </li>

        <li class="nav-item">
            <a class="nav-link" href="/register">Register</a>
        </li>
        </ul>
    </div>
</nav>

    <div class="container mt-2">
        <div class="container d-flex justify-content-center">
            <div class="col-lg-6 col-md-8 col-sm-10" style="margin-top:50px">

                <h5 class="text-center">Login Page</h5>
                <p class="text-center">Fill this page to login to your account.</p>
                <hr>
                <br>

                <form @submit.prevent="loginUser()">

                    <div class="form-group" style="display: flex; flex-direction: column; align-items: center;">

                        <label class="col-sm-2 col-form-label" for="username" >Username</label>
                        
                        <input 
                            type="text" 
                            class="form-control" 
                            id="username" 
                            v-model="username" 
                            required
                            placeholder="Enter username" 
                            style="width:300px; margin-top:7px">
                    </div>
                    
                    <br>

                    <div class="form-group" style="display: flex; flex-direction: column; align-items: center;">

                        <label class="col-sm-2 col-form-label" for="password" >Password</label>

                        <input 
                            type="password" 
                            class="form-control" 
                            id="password" 
                            v-model="password" 
                            required
                            placeholder="Enter password" 
                            style="width:300px; margin-top:7px">
                    </div>

                    <div class="form-group d-flex justify-content-center">
                        <button 
                            type="submit" 
                            class="btn btn-outline-primary mt-4" 
                            @click.prevent="loginUser()">Login</button>
                    </div>
                    
                    
                </form>
            </div>
        </div>
    </div>

</div>
    
</template>


<script>
import axios from "axios";

export default {
    name: "LoginView",
    data() {
        return {
            username: "",
            password: "",
        };
    },
    methods: {
        loginUser() {
            if (!this.username || !this.password) {
                alert("Please enter both the username and the password !!")
            }

            axios
                .post('http://127.0.0.1:5000/api/login', {
                    username: this.username,
                    password: this.password,
                })

                .then((response) => {
                    if (response.data.status === "success") {
                        const access_token = response.data.access_token;
                        const refresh_token = response.data.refresh_token;
                        const username = response.data.username;


                        localStorage.setItem("access_token", access_token);
                        localStorage.setItem("refresh_token", refresh_token);
                        localStorage.setItem("username", username)

                        alert("Successfully Logged in !!")
                        this.$router.push("/feed");
                    } 

                    else {
                        alert("Invalid credentials !!")
                    }
                    
                })

                .catch((error) => {
                    console.error(error);
                    alert("An error occurred while logging in !!");
                });
        },
    },
};
</script>
