<template>
    <div>
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
                        <li class="nav-item active">
                            <a class="nav-link" href="#">Home</a>
                        </li>

                        <li class="nav-item">
                            <a class="nav-link" href="/register">Register</a>
                        </li>

                        <li class="nav-item">
                            <a class="nav-link" href="/login">Login</a>
                        </li>
                        
                    </ul>
                </div>
            </nav>
        </div>

        <div class="container mt-5">
            <h2>Welcome to my blog-lite application !!</h2>
            <p class="lead" style="max-width: 50%">Thank you for visiting my application.
                <br>
                <br>
                As a recent graduate of the MAD 2 course, I am excited to showcase my blogging application. This project
                serves as
                a
                testament to my skills in web development and my passion for creating dynamic, user-friendly websites.

                <br>
                <br>

                I have invested a significant amount of time and energy into developing this platform and I am confident
                that you
                will
                find it both engaging and useful. Whether you are a seasoned blogger or just starting out, I am sure you
                will
                appreciate
                the ease and functionality of this application.
            </p>
        </div>


    </div>
</template>

<script>
import axios from "axios";
export default {
    name: "welcome-page",
    data() {
        return {
            msg: ""
        };
    },
    methods: {
        getResponse() {
            const path = "http://localhost:5000/welcome";
            axios.get(path)
                .then((res) => {
                    console.log(res.data)
                    this.msg = res.data;
                })
                .catch((err) => {
                    console.error(err);
                });
        },
    },
    created() {
        this.getResponse();
    },

    mounted() {
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


<style>
.navbar-nav {
    margin-left: auto;
    margin-right: 50px;
}

.navbar-brand {
    margin-left: 50px;
}</style>
