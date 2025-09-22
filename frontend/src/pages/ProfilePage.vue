<template>
    <div class="profile-container">
      <h1 class="my-4">User Profile</h1>
  
      <!-- Display Profile Information -->
      <div class="profile-info card mb-4" v-if="user">
        <div class="card-body">
          <h2 class="card-title">Profile Information</h2>
  
          <!-- Name -->
          <div class="profile-field">
            <p><strong>Name:</strong></p>
            <input
              type="text"
              class="form-control"
              :readonly="!isEditing"
              v-model="profileData.name"
            />
          </div>
  
          <!-- Email -->
          <div class="profile-field">
            <p><strong>Email:</strong></p>
            <input
              type="email"
              class="form-control"
              :readonly="!isEditing"
              v-model="profileData.email"
            />
          </div>
  
          <!-- Date of Birth -->
          <div class="profile-field">
            <p><strong>Date of Birth:</strong></p>
            <input
              type="date"
              class="form-control"
              :readonly="!isEditing"
              v-model="profileData.dob"
            />
          </div>
  
          <!-- Hobbies -->
          <div class="profile-field">
            <p><strong>Hobbies:</strong></p>
            <div v-if="isEditing">
              <select class="form-select" v-model="profileData.hobbies" multiple>
                <option v-for="hobby in allHobbies" :key="hobby.id" :value="hobby.id">
                  {{ hobby.name }}
                </option>
              </select>
              <small class="form-text text-muted mt-2">
                Select or deselect hobbies from the list above. Hold Ctrl (Cmd on Mac) to select multiple options.
              </small>
            </div>
            <div v-else>
              <ul class="list-group">
                <li class="list-group-item" v-for="hobby in user.hobbies" :key="hobby.id">
                  {{ hobby.name }}
                </li>
              </ul>
            </div>
          </div>
  
          <!-- Edit, Save, and Change Password Buttons -->
          <div class="form-actions mt-4">
            <button class="btn btn-primary" v-if="!isEditing" @click="enableEditing">
              Edit Profile
            </button>
            <button
              class="btn btn-success"
              v-if="isEditing"
              :disabled="!hasChanges"
              @click="saveChanges"
            >
              Save Changes
            </button>
            <button class="btn btn-secondary" v-if="!isEditing" @click="updatePassword">
              Change Password
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { ref, computed, onMounted } from 'vue';
  
  interface Hobby {
    id: number;
    name: string;
  }
  
  interface User {
    id: number;
    name: string;
    email: string;
    dob: string;
    hobbies: Hobby[];
  }
  
  export default {
    name: 'ProfilePage',
    setup() {
      const user = ref<User | null>(null);
      const allHobbies = ref<Hobby[]>([]);
      const profileData = ref<{
        name: string;
        email: string;
        dob: string;
        hobbies: number[];
      }>({
        name: '',
        email: '',
        dob: '',
        hobbies: [],
      });
      const isEditing = ref(false);
      const originalData = ref({});
  
      const getUsernameFromLocalStorage = () => {
        return localStorage.getItem('username');
      };
  
      const fetchProfile = async () => {
        const username = getUsernameFromLocalStorage();
        if (username) {
          const response = await fetch(`http://127.0.0.1:8000/profile/${username}/`);
          const data = await response.json();
          user.value = {
            ...data.user,
            hobbies: data.hobbies,
          };
          profileData.value = {
            name: data.user.name,
            email: data.user.email,
            dob: data.user.dob,
            hobbies: data.hobbies.map((hobby: Hobby) => hobby.id),
          };
          originalData.value = JSON.parse(JSON.stringify(profileData.value));
        }
      };
  
      const fetchHobbies = async () => {
        const response = await fetch('http://127.0.0.1:8000/hobbies/');
        const data = await response.json();
        allHobbies.value = data.Hobbies;
      };
  
      onMounted(() => {
        fetchProfile();
        fetchHobbies();
      });
  
      const enableEditing = () => {
        isEditing.value = true;
      };
  
      const saveChanges = async () => {
        const username = getUsernameFromLocalStorage();
        if (username) {
          const response = await fetch(`http://127.0.0.1:8000/profile/${username}/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(profileData.value),
          });
  
          const data = await response.json();
          if (data.success) {
            alert('Profile updated successfully!');
            isEditing.value = false;
            fetchProfile();
          } else {
            alert('Error updating profile.');
          }
        }
      };
  
      const updatePassword = async () => {
  const newPassword = prompt('Enter your new password:');
  const username = getUsernameFromLocalStorage(); // Retrieve the username from localStorage

  if (newPassword && username) {
    try {
      const response = await fetch(`http://127.0.0.1:8000/profile/${username}/password/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password: newPassword }),
      });

      const data = await response.json();

      if (response.ok && data.success) {
        alert('Password updated successfully!');
      } else {
        alert(`Error updating password: ${data.error || 'Unknown error'}`);
      }
    } catch (error: unknown) {
      if (error instanceof Error) {
        alert(`Error updating password: ${error.message}`);
      } else {
        alert('An unknown error occurred while updating the password.');
      }
    }
  } else if (!username) {
    alert('Username not found. Please log in again.');
  } else {
    alert('Password change canceled.');
  }
};


  
      const hasChanges = computed(() => {
        return JSON.stringify(profileData.value) !== JSON.stringify(originalData.value);
      });
  
      return {
        user,
        allHobbies,
        profileData,
        isEditing,
        hasChanges,
        enableEditing,
        saveChanges,
        updatePassword,
      };
    },
  };
  </script>
  
  <style scoped>
  .profile-container {
    padding: 30px;
    max-width: 900px;
    margin: 0 auto;
    background-color: #f9f9f9;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
  }
  
  h1 {
    font-size: 28px;
    color: #333;
    text-align: center;
    margin-bottom: 40px;
    font-weight: bold;
  }
  
  .profile-info.card {
    background-color: #ffffff;
    border: none;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    padding: 20px;
  }
  
  .card-title {
    font-size: 22px;
    font-weight: bold;
    color: #555;
    border-bottom: 1px solid #ddd;
    padding-bottom: 10px;
    margin-bottom: 20px;
  }
  
  /* Profile Fields */
  .profile-field {
    margin-bottom: 20px;
  }
  
  .profile-field p {
    font-weight: bold;
    margin-bottom: 5px;
    color: #555;
  }
  
  .profile-field input,
  .profile-field select {
    width: 100%;
    padding: 10px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 5px;
    outline: none;
    transition: border-color 0.3s ease;
  }
  
  .profile-field input:focus,
  .profile-field select:focus {
    border-color: #007bff;
  }
  
  .profile-field .list-group-item {
    color: #555;
    padding: 8px 12px;
    margin-bottom: 5px;
    border: 1px solid #ddd;
    border-radius: 5px;
    background-color: #f8f8f8;
  }
  
  .profile-field .list-group-item:last-child {
    margin-bottom: 0;
  }
  
  .profile-field .form-text {
    font-size: 13px;
    color: #999;
    margin-top: 5px;
  }
  
  .btn {
    padding: 10px 18px;
    font-size: 16px;
    border-radius: 5px;
    transition: background-color 0.3s ease;
  }
  
  .btn-primary {
    background-color: #007bff;
    color: #fff;
    border: none;
  }
  
  .btn-primary:hover {
    background-color: #0056b3;
  }
  
  /* Success Button */
  .btn-success {
    background-color: #28a745;
    color: #fff;
    border: none;
  }
  
  .btn-success:hover {
    background-color: #218838;
  }
  
  /* Secondary Button */
  .btn-secondary {
    background-color: #6c757d;
    color: #fff;
    border: none;
  }
  
  .btn-secondary:hover {
    background-color: #5a6268;
  }
  
  .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 15px;
    margin-top: 20px;
  }
  </style>