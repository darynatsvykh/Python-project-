<template>
  <form class="login-container" @submit.prevent="login">
    <div>
      <h2 class="login">LOGIN</h2>

      <label for="username"> Username:</label>
      <input
        v-model="username"
        type="text"
        class="form-control"
        placeholder="username"
        required
      />

      <label for="password"> Password:</label>
      <input
        v-model="password"
        type="password"
        class="form-control"
        placeholder="password"
        required
      />
    </div>
    <p class="signup">
      Don't have an account? Sing up
      <router-link class="signup-link" :to="{ name: 'Sign Page' }"> here </router-link>
    </p>
    <button class="btn btn-success btn-block my-2" type="submit">Login</button>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </form>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import axios from "axios";

export default defineComponent({
  name: "Login Page",
  data() {
    return {
      username: "",
      password: "",
      csrfToken: "",
      errorMessage: ""
    };
  },

  created() {
    const isAuthenticated = localStorage.getItem("isAuthenticated");
    if (isAuthenticated === "true") {
      this.$router.push({ name: "Main Page" });
    }

    this.getCsrfToken();
  },

  methods: {
    async getCsrfToken() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/csrf-token/", 
          {
            withCredentials: true,
          }
        );

        this.csrfToken = response.data.csrfToken || "";

        console.log("CSRF Token retrieved:", this.csrfToken);
      } catch (error: any) {
        console.error("Failed to retrieve CSRF token:", error.response || error);
      }
    },

    async login() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/login/",
          {
            username: this.username,
            password: this.password
          },
          {
            headers: {
              "X-CSRFToken": this.csrfToken,
              "Content-Type": "application/json"
            },
            withCredentials: true // Ensures the cookies are sent with the request
          }
        );

        if (response.status === 200) {
          localStorage.setItem("user_id", response.data.user.id);
          console.log("id: " + response.data.user.id);

          localStorage.setItem("isAuthenticated", "true");
          localStorage.setItem("username", this.username);
          this.$router.push({ name: "Main Page" });
          location.reload();
        }
      } catch (error: any) {
        this.errorMessage = error.response?.data?.error || "Login failed";
      }
    }
  }
});
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 0 auto;
  justify-content: center;
  background-color: aliceblue;
  font-family: "Mulish", sans-serif;
  transition: 0.3s all ease-in-out;
  border-radius: 5px;
  padding: 25px;
}
.login,
.signup {
  text-align: center;
}
.error {
  color: red;
}
.signup-link {
  text-decoration: underline;
  color: brown;
  padding: 10px;
}
.btn {
  width: 100%;
  padding: 10px;
  background-color: grey;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>