<template>
    <main class="container pt-4">
      <div class="navbar">
        <router-link v-if="isAuthenticated" class="nav-link" :to="{name: 'Main Page'}">
          Home
        </router-link>
        
        <router-link v-if="isAuthenticated" class="nav-link" :to="{name: 'Hobbies Page'}">
          Hobbies Page
        </router-link>
        
        <router-link v-if="isAuthenticated" class="nav-link" :to="{ name: 'Profile Page' }">
          Profile Page
        </router-link>
        
        <router-link v-if="!isAuthenticated" class="nav-link" :to="{name: 'Login Page'}">
          Login
        </router-link>
        
        <button v-else @click="logout" class="logout-button">Logout</button>
      </div>
      
      <!-- Main content -->
      <RouterView class="main-content" />
    </main>
  </template>
  
<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { RouterView, useRouter } from "vue-router";
import axios from "axios";

export default defineComponent({
    components: { RouterView },
    setup() {
        const isAuthenticated = ref(false);
        const router = useRouter();
        const csrfToken = ref("");
        const checkAuth = () => {
            isAuthenticated.value = localStorage.getItem("isAuthenticated") === "true";
        };
        const getCsrfToken = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:8000/csrf-token/", {
                    withCredentials: true, // Ensures cookies (like CSRF cookie) are sent with the request
                });
                csrfToken.value = response.data.csrfToken || "";
                console.log("CSRF Token retrieved:", csrfToken.value);
            } catch (error: any) {
                console.error("Failed to retrieve CSRF token:", error.response || error);
            }
        };
        const logout = async () => {
            try {
                await axios.post(
                    "http://127.0.0.1:8000/logout/", // Django logout endpoint
                    {},
                    {
                        headers: {
                            "X-CSRFToken": csrfToken.value, // Include CSRF token in the request
                            "Content-Type": "application/json",
                        },
                        withCredentials: true, // Ensure cookies are sent
                    }
                );
                // Clear local session storage
                localStorage.removeItem("isAuthenticated");
                localStorage.removeItem("username");
                isAuthenticated.value = false;
                // Redirect to login page
                router.push({ name: "Login Page" });
            } catch (error) {
                console.error("Logout failed", error);
            }
        };
        onMounted(async () => {
            await getCsrfToken();
            checkAuth();
        });
        return { isAuthenticated, logout };
    },
    // methods: {        
    //     async logoutUser() {
    //         try {
    //             await axios.post(
    //                 "http://127.0.0.1:8000/logout/",
    //                 {},
    //                 {
    //                     headers: 
    //                     {
    //                         "X-CSRFToken": csrfToken.value, // Include CSRF Token
    //                         "Content-Type": "application/json",
    //                     }
    //                 },
    //             );
    //             // Remove user session/token
    //             localStorage.removeItem("user");
    //             // Redirect to login page
    //             this.$router.push("/");
    //         } catch (error) {
    //             console.error("Logout failed", error);
    //         }
    //     },
    // }
});

</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding-top: 20px;
  padding-bottom: 20px;
}
.navbar {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}
.nav-link {
  font-size: 16px;
  font-weight: 600;
  text-decoration: none;
  color: #2c3e50;
  padding: 10px;
  transition: color 0.3s, border-bottom 0.3s;
}

.nav-link:hover {
  color: #3498db;
  border-bottom: 2px solid #3498db;
}

.logout-button {
  padding: 10px 20px;
  background-color: #e74c3c;
  color: white;
  font-size: 16px;
  font-weight: 600;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.logout-button:hover {
  background-color: #c0392b;
}

.main-content {
  margin-top: 20px;
  min-height: 400px;
  padding: 20px;
  background-color: #f4f6f7;
  border-radius: 8px;
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
}
.container{
    background-color: azure;
}
</style>
