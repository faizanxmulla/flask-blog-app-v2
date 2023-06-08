import Vue from "vue";
import VueRouter from "vue-router";
import WelcomeView from "../components/WelcomeView.vue";

// Navbar route 
// import NavBar from "../components/Navbar.vue";


// Auth routes
import RegisterView from "../views/auth/RegisterView.vue";
import LoginView from "../views/auth/LoginView.vue";

// posts routes
import CreatePostView from "../views/posts/CreatePostView.vue";
import UpdatePostView from "../views/posts/UpdatePostView.vue";
import DeletePostView from "../views/posts/DeletePostView";

// users/accounts routes 
import UpdateAccountView from "../views/accounts/UpdateAccountView.vue";
import DeleteAccountView from "../views/accounts/DeleteAccountView";
import SearchAccountView from "../views/accounts/SearchAccountView.vue";

// comments routes
import CommentView from "../views/comments/CommentView.vue";
import UpdateCommentView from "../views/comments/UpdateCommentView.vue";
import DeleteCommentView from "../views/comments/DeleteCommentView";

// follow routes 
import FollowersView from "../views/follow/FollowersView.vue";
import FollowingView from "../views/follow/FollowingView.vue";

// feed route 
import FeedView from "../views/posts/FeedView.vue"

// profile route 
import ProfileView from "../views/accounts/ProfileView.vue"



Vue.use(VueRouter);

const routes = [
    {
        path: "/",
        name: "Welcome-Page",
        component: WelcomeView,
    },
    {
        path: "/register",
        name: "Registration-Page",
        component: RegisterView,
    },
    {
        path: "/login",
        name: "Login-Page",
        component: LoginView,
    },
    {
        path: "/create-post",
        name: "Create-Post-Page",
        component: CreatePostView,
    },
    {
        path: "/post/:post_id/update",
        name: "Update-Post-Page",
        component: UpdatePostView,
        props: true,
    },
    {
        path: "/post/:post_id/delete",
        name: "Delete-Post-Page",
        component: DeletePostView,
    },
    {
        path: "/update-account",
        name: "Update-Account-Page",
        component: UpdateAccountView,
    },
    {
        path: "/delete-account",
        name: "Delete-Account-Page",
        component: DeleteAccountView,
    },
    {
        path: "/search",
        name: "Search-Account-Page",
        component: SearchAccountView,
    },
    {
        path: "/post/:post_id/comment",
        name: "Comments-Page",
        component: CommentView,
    },
    {
        path: "/post/:post_id/comment/:comment_id/update",
        name: "Update-Comment-Page",
        component: UpdateCommentView,
    },
    {
        path: "/post/:post_id/comment/:comment_id/delete",
        name: "Delete-Comment-Page",
        component: DeleteCommentView,
    },
    {
        path: "/followers/:username",
        name: "Followers-Page",
        component: FollowersView,
    },
    {
        path: "/following/:username",
        name: "Following-Page",
        component: FollowingView,
    },
    {
        path: "/feed",
        name: "Feed-Page",
        component: FeedView,
    },
    {
        path: "/profile/:username",
        name: "Profile-Page",
        component: ProfileView,
    },
];

const router = new VueRouter({
    mode: "history",
    base: process.env.BASE_URL,
    routes,
});

export default router;
