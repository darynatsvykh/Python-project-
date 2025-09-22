<template>
    <div class="signup-container">
      <h2>Sign Up</h2>
      <form @submit.prevent="submitSignup">
        <div class="form-group">
          <label for="username">Username:</label>
          <input
            v-model="formData.username"
            type="text"
            name="username"
            placeholder="Enter your username"
            class="form-control"
            required
          />
        </div>
          <div class="form-group">
          <label for="name"> First Name:</label>
          <input
            v-model="formData.name"
            type="text"
            name="name"
            placeholder="Enter your name"
            class="form-control"
            required
          />
        </div>
        <div class="form-group">
          <label for="surname"> Surame:</label>
          <input
            v-model="formData.surname"
            type="text"
            name="surname"
            placeholder="Enter your surname"
            class="form-control"
            required
          />
        </div>
        <div class="form-group">
          <label for="email">Email</label>
          <input
            v-model="formData.email"
            type="text"
            name="email"
            placeholder="Enter your email"
            class="form-control"
            required
          />
        </div>
        <div class="form-group">
          <label for="dob">Date of birth</label>
          <input
            v-model="formData.dob"
            type="date"
            name="dob"
            class="form-control"
            required
          />
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input
            v-model="formData.password"
            type="password"
            name="password"
            placeholder="Enter your password"
            class="form-control"
            required
          />
        </div>
        <div class="form-group">
          <label for="confirmPassword">Confirm Password:</label>
          <input
            v-model="formData.confirmPassword"
            type="password"
            name="confirmPassword"
            placeholder="Confirm your password"
            class="form-control"
            required
          />
        </div>
  
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        <button type="submit" class="btn btn-primary">Sign Up</button>
      </form>
    </div>
  </template>
  
  <script lang="ts">
  import axios from "axios";
  
  export default {
    name: "SignupForm",
    data() {
      return {
        formData: {
          username: "",
          name: "",
          surname: "",
          email: "",
          dob: "",
          password: "",
          confirmPassword: "",
        },
        errorMessage: "",
        csrfToken: "",
      };
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
          this.csrfToken = response.data.csrfToken || ""; // Save the CSRF token
          console.log("CSRF token retrieved:", this.csrfToken);
        } catch (error) {
          console.error("Failed to retrieve CSRF token:", error);
        }
      },

      async submitSignup() {
        if (this.formData.password !== this.formData.confirmPassword) {
          this.errorMessage = "Passwords do not match :( try again!";
          return;
        }
  
        this.errorMessage = "";
  
        const payload = {
          username: this.formData.username,
          password: this.formData.password,
          name: this.formData.name,
          surname: this.formData.surname,
          email: this.formData.email,
          dob: this.formData.dob,
        };
  
        try {
          const response = await axios.post(
            "http://127.0.0.1:8000/signup/",
            payload,
            
          );
          console.log("User registered:", response.data);
  
          this.$router.push({name: "Login Page"});
        } catch (error: any) {
          this.errorMessage = error.response?.data?.detail || "An error occurred during registration :( Please try again";
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .signup-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 10px;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  h2 {
    text-align: center;
    margin-bottom: 20px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .form-control {
    width: 100%;
    padding: 10px;
    margin-top: 5px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .error {
    color: red;
    font-size: 14px;
    text-align: center;
  }
  
  .btn {
    width: 100%;
    padding: 10px;
    background-color:plum;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .btn:hover {
    background-color: #0056b3;
  }
  </style>
  
  
