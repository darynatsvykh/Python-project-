<template>
  <div class="container">
    <Greeting />

    <div class="filters-container">
      <div class="filters">
        <label for="minAge" class="filter-label">Min Age:</label>
        <input type="number" v-model.number="filters.minAge" id="minAge" class="filter-input" />

        <label for="maxAge" class="filter-label">Max Age:</label>
        <input type="number" v-model.number="filters.maxAge" id="maxAge" class="filter-input" />

        <button @click="filterUsers" class="filter-button">Filter</button>
        <button class="filter-button" @click="clearFilters">Clear Filters</button>
      </div>
    </div>

    <!-- Users Table -->
    <table class="table table-striped">
      <thead>
        <tr>
          <th>#</th>
          <th>Name</th>
          <th>Email</th>
          <th>Date of Birth</th>
          <th>Hobbies</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="(user, index) in filteredUsers" :key="user.id">
          <td>{{ index + 1 }}</td>
          <td>{{ user.name }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.dob || 'N/A' }}</td>
          <td>
            <ul v-if="user.hobbies.length > 0">
              <li v-for="(hobby, hobbyIndex) in user.hobbies" :key="hobbyIndex">
                {{ hobby }}
              </li>
            </ul>
            <p v-else>No hobbies have been picked.</p>
          </td>
          <td>
            <button
              v-if="!sentFriendRequests.includes(user.id)"
              @click="sendFriendRequest(user.id)"
              class="friend-request-button"
            >
              Send Friend Request
            </button>
            <span v-else class="request-pending">Pending</span>
          </td>
        </tr>
      </tbody>
    </table>
    <!-- Pagination -->
    <div class="pagination-controls">
      <button :disabled="!pagination.has_previous" @click="changePage(pagination.current_page - 1)">
        Previous
      </button>
      <span>Page {{ pagination.current_page }} of {{ pagination.total_pages }}</span>
      <button :disabled="!pagination.has_next" @click="changePage(pagination.current_page + 1)">
        Next
      </button>
    </div>

    <!-- Similar Users Button -->
    <div class="similar-users-section">
      <button @click="fetchSimilarUsers" class="fetch-similar-users-button">
        Show Users with Similar Hobbies
      </button>
      <button   @click="hideSimilarUsers" class="fetch-similar-users-button">
        Hide this section
      </button>
    </div>

    <!-- Similar Users Table -->
    <table v-if="showSimilarUsers > 0" class="table table-striped">
      <thead>
        <tr>
          <th>#</th>
          <th>Name</th>
          <th>Email</th>
          <th>Date of Birth</th>
          <th>Hobbies</th>
          <th>Number of Common Hobbies</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="(user, index) in similarUsers" :key="user.id">
          <td>{{ index + 1 }}</td>
          <td>{{ user.name }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.dob || 'N/A' }}</td>
          <td>
            <ul>
              <li v-for="(hobby, hobbyIndex) in user.hobbies" :key="hobbyIndex">
                {{ hobby }}
              </li>
            </ul>
          </td>
          <td>{{ user.common_hobby_count }}</td>
          <td>
            <button @click="sendFriendRequest(user.id)" class="friend-request-button">
              Send Friend Request
            </button>
            </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
  
<script lang="ts">
import { defineComponent } from "vue";
import axios from "axios";
import Greeting from "./Greeting.vue";

export default defineComponent({
  name: "UsersTable",
  components: {
    Greeting,
  },
  data() {
    return {
      users: [],
      csrfToken: "",
      filters: {
        minAge: null,
        maxAge: null,
      },
      pagination: {
        current_page: 1,
        total_pages: 1,
        has_next: false,
        has_previous: false,
      },
      page_size: 10,
      isFiltering: false,
      filteredUsers: [],
      similarUsers: [],
      showSimilarUsers: false,
      sentFriendRequests: [] as number[],
    };
  },

  async created() {
    await this.fetchUsers();

    try {
      const response = await axios.get("http://127.0.0.1:8000/users/");
      this.users = response.data.users;
      this.filteredUsers = [...this.users];
    } catch (error) {
      console.error("Error fetching users:", error);
    }
  },
  watch: {
    filters: {
      handler(){
        this.fetchUsers();
      },
      deep: true, 
    },
  },
  methods: {
    getCsrfToken() {
      const csrfCookie = document.cookie
        .split("; ")
        .find((row) => row.startsWith("csrftoken="));
      return csrfCookie ? csrfCookie.split("=")[1] : "";
    },

    async fetchUsers() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/users/");
        this.users = response.data.users;
        this.filteredUsers = [...this.users];
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    },
    async fetchUsers(page = 1) { 
    try {
      const response = await axios.get("http://127.0.0.1:8000/users/", {
        params: {
          page,
          page_size: this.page_size,
          min_age: this.filters.minAge,
          max_age: this.filters.maxAge,
        },
      });
      
      this.users = response.data.users;
      this.filteredUsers = this.users;
      this.pagination = response.data.pagination || {
        current_page: 1,
        total_pages: 1,
        has_next: false,
        has_previous: false,
      };
    } catch (error) {
      console.error("Error fetching users:", error);
      this.pagination = {
        current_page: 1,
        total_pages: 1,
        has_next: false,
        has_previous: false,
      };
    }
  },
    async changePage(page) {
      if (page > 0 && page <= this.pagination.total_pages) {
        await this.fetchUsers(page);
      }
    },
    hideSimilarUsers() {
      if (!this.showSimilarUsers) {
        this.fetchSimilarUsers(); // Fetch only when opening
      }
      this.showSimilarUsers = !this.showSimilarUsers; // Toggle visibility
    },
  
    calculateAge(dateOfBirth) {
      const today = new Date();
      const dob = new Date(dateOfBirth);
      let age = today.getFullYear() - dob.getFullYear();
      const monthDifference = today.getMonth() - dob.getMonth();
      if (monthDifference < 0 || (monthDifference === 0 && today.getDate() < dob.getDate())) {
        age--;
      }
      return age;
    },

    filterUsers() {
    const { minAge, maxAge } = this.filters;
    console.log("Filter criteria:", { minAge, maxAge });

    this.filteredUsers = this.users.filter((user) => {
      const age = this.calculateAge(user.dob);
      return (!minAge || age >= minAge) && (!maxAge || age <= maxAge);
    });
    console.log("Filtered users:", this.filteredUsers);
  },

  async sendFriendRequest(recipientId: number) {
    try {
      const senderId = localStorage.getItem("user_id");
      if (!senderId) {
        console.error("User ID not found in localStorage.");
        return;
      }

      await axios.post(
        "http://127.0.0.1:8000/send-friend-request/",
        {
          sender_id: senderId,
          recipient_id: recipientId,
        },
        {
          headers: {
            "X-CSRFToken": this.csrfToken, // Include the CSRF token in the headers
          },
          withCredentials: true,
        }
      );

      // Add this user ID to the list of sent friend requests
      this.sentFriendRequests.push(recipientId);

      alert("Friend request sent successfully!");
    } catch (error) {
      console.error("Error sending friend request:", error);
      alert("Failed request has already been sent.");
    }
  },

    async fetchSimilarUsers() {
      try {
        const userId = localStorage.getItem("user_id");
        if (!userId) {
          console.error("User ID not found.");
          return;
        }

        const response = await axios.get(`http://127.0.0.1:8000/similar_users/${userId}/`);
        this.similarUsers = response.data.similar_users;
        this.showSimilarUsers = true;
      } catch (error) {
        console.error("Error fetching similar users:", error);
      }
    },

    async clearFilters() {
      this.isFiltering = false;
      this.filters = { minAge: null, maxAge: null }; // Reset filters
      await this.fetchUsers(1);
    },
  },
});
</script>
  
  <style scoped>
  .container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Arial', sans-serif;
  }
.page-title {
  text-align: center;
  font-size: 36px;
  color:black;
  margin-bottom: 20px;
  }
.filters-container {
  margin-bottom: 20px;
  text-align: center;
  display: flex;
  justify-content: center;
  gap: 10px;
  }

.filters {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 10px;
  }
.filter-label {
  font-size: 16px;
  font-weight: bold;
  margin-right: 8px;
  }
.filter-input {
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 120px;
  }
.filter-button {
  padding: 8px 16px;
  font-size: 16px;
  background-color:rgb(159, 108, 207);
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  }
  .table {
    width: 100%;
    margin: 20px auto;
    border-collapse: collapse;
    border-radius: 8px;
    overflow: hidden;
  }
  .table th,
  .table td {
    padding: 10px;
    text-align: left;
    border: 1px solid #ddd;
  }
  .table th {
  background-color: #f4f4f4;
  font-weight: bold;
  }
  .friend-request-button {
  padding: 8px 12px;
  font-size: 14px;
  background-color: rgb(108, 159, 207);
  color: white;
  border-radius: 4px;
  border: none;
  cursor: pointer;
}
.friend-request-button:hover {
  background-color: rgb(80, 120, 160);
}

.similar-users-section {
  text-align: center;
  margin: 20px 0;
  justify-content: center;
  gap: 10px;
  display: flex;
}

.fetch-similar-users-button {
  padding: 8px 16px;
  font-size: 16px;
  background-color: rgb(108, 159, 207);
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.fetch-similar-users-button:hover {
  background-color: rgb(80, 120, 160);
}

.pagination-controls {
display: flex;
justify-content: center;
gap: 10px;
}
.pagination-controls button {
padding: 6px 12px;
background-color: rgb(159, 108, 207);
color: #fff;
border: none;
border-radius: 4px;
cursor: pointer;
}
.pagination-controls button:disabled {
background-color: #ccc;
cursor: not-allowed;
}
.request-pending {
  display: inline-block;
  background-color: #ffd700; /* Gold-like background */
  color: #333; /* Dark text color */
  padding: 6px 12px;
  border-radius: 5px;
  font-weight: bold;
  font-size: 13px;
  text-align: center;
  text-transform: uppercase;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  animation: fadeIn 0.5s ease;
}
</style>
  
