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
                aria-label="Toggle navigation">
                
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/">Home</a>
                    </li>

                    <li class="nav-item">
                        <a class="nav-link" href="/login">Login</a>
                    </li>
                </ul>
            </div>
        </nav>

        <div class="container mt-2">
            <div class="container d-flex justify-content-center">
                <div class="col-lg-6 col-md-8 col-sm-10" style="margin-top: 20px">
                    <h5 class="text-center">Registration Page</h5>
                    <p class="text-center">Fill this page to create an account.</p>
                    <hr />
                    <br />

                    <form @submit.prevent="registerUser()">
                        <div class="form-group" style="display: flex; flex-direction: column; align-items: center;">
                            <label class="col-sm-2 col-form-label" for="username" >Username</label>
                            <input 
                                type="text" 
                                class="form-control" 
                                id="username" 
                                v-model="username" 
                                required
                                placeholder="Enter username" 
                                style="width: 50%; margin-top: 7px" />
                        </div>

                        <div class="form-group" style="display: flex; flex-direction: column; align-items: center;">

                            <label class="col-sm-2 col-form-label" for="email" >Email</label>

                                <input 
                                    type="email" 
                                    class="form-control" 
                                    id="email" 
                                    v-model="email" 
                                    required
                                    placeholder="Enter email" 
                                    style="width: 50%; margin-top: 7px" />
                        </div>

                        <div class="form-group" style="display: flex; flex-direction: column; align-items: center;">

                            <label class="col-sm-2 col-form-label" for="password" >Password</label>

                            <input 
                                type="password" 
                                class="form-control" 
                                id="password" 
                                v-model="password" 
                                required
                                placeholder="Enter password" 
                                style="width: 50%; margin-top: 7px" />
                        </div>

                        <div class="form-group" style="display: flex; flex-direction: column; align-items: center;">

                            <label class="col-sm-2 col-form-label" for="confirm_password" >  Confirm Password</label>

                            <input 
                                type="password" 
                                class="form-control" 
                                id="confirm_password" 
                                v-model="confirmPassword"
                                required 
                                placeholder="Confirm Password" 
                                style="width: 50%; margin-top: 7px" />
                        </div>

                        <div class="form-group d-flex justify-content-center">
                            <button 
                                type="submit" 
                                class="d-flex justify-content-center btn btn-outline-primary mt-4" 
                                @click.prevent="registerUser()"> Register </button>
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
    name: "RegisterView",
    data() {
        return {
            username: "",
            email: "",
            password: "",
            confirmPassword: "",
        };
    },
    methods: {
        registerUser() {
            if (!this.username || !this.email || !this.password || !this.confirmPassword) {
                alert("All fields are required !!");
                return;
            }

            if (!this.email.includes("@") || !this.email.endsWith(".com")) {
                alert("Invalid email format !! Email must include '@' and end with '.com'");
                return;
            }

            if (this.password != this.confirmPassword) {
                alert("Passwords don't match !!");
                return;
            }

            axios
                .post("http://127.0.0.1:5000/api/register", {
                    username: this.username,
                    email: this.email,
                    password: this.password,
                    confirm_password: this.confirmPassword,
                })
                .then(() => {
                    alert("Successfully Registered !!")
                    this.$router.push("/login");
                })
                .catch((error) => {
                    console.error(error);
                    alert("An error occurred while registering the user");
                });
        },
    },
    
};
</script>
