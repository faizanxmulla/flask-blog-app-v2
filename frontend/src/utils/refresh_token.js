import axios from "axios";

async function refreshAccessToken() {
    // Get the refresh token from local storage
    let refresh_token = localStorage.getItem("refresh_token");

    // Set the Authorization header of the axios instance
    axios.defaults.headers.common["Authorization"] = "Bearer " + refresh_token;

    try {
        // Send a POST request to the server to refresh the access token
        let response = await axios.post("http://127.0.0.1:5000/api/token/refresh");

        // Get the new access token from the response
        let n_access_token = response.data.access_token;

        // Store the new access token in local storage
        localStorage.setItem("access_token", n_access_token);

        // Update the Authorization header of the axios instance
        axios.defaults.headers.common["Authorization"] = "Bearer " + n_access_token;
        
    } catch (error) {
        // Handle errors (e.g. invalid refresh token)
        console.error(error);
    }
}

export default refreshAccessToken;
