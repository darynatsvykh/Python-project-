<template>
  <div>
    <div class="mb-3">
      <button 
        class="btn btn-primary" 
        @click="showAddHobbyModal = true"
      >
        Add Hobby
      </button>
    </div>

    <table class="table">
      <thead>
        <tr>
          <th>#</th>
          <th>Hobby Name</th>
          <th>Description</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(hobby, index) in hobbiesStore.hobbies" :key="hobby.id">
          <td>{{ index + 1 }}</td>
          <td>{{ hobby.name }}</td>
          <td>{{ hobby.description }}</td>
          <td>
            <button 
              class="btn btn-danger btn-sm" 
              @click="handleDeleteHobby(hobby.id)"
            > 
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Modal for Adding Hobby -->
    <div 
      v-if="showAddHobbyModal" 
      class="modal d-block" 
      tabindex="-1"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add Hobby</h5>
            <button 
              type="button" 
              class="btn-close" 
              @click="closeModal"
            ></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label for="hobbyName" class="form-label">Hobby Name</label>
              <input 
                id="hobbyName" 
                v-model="newHobby.name" 
                class="form-control" 
                placeholder="Enter hobby name" 
                required
              />
            </div>
            <div class="mb-3">
              <label for="hobbyDescription" class="form-label">Description</label>
              <textarea 
                id="hobbyDescription" 
                v-model="newHobby.description" 
                class="form-control" 
                placeholder="Enter hobby description"
              ></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button 
              type="button" 
              class="btn btn-secondary" 
              @click="closeModal"
            >
              Close
            </button>
            <button 
              type="button" 
              class="btn btn-primary" 
              @click="handleAddHobby"
            >
              Save Hobby
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { useHobbiesStore } from '../store/hobbiesStore';

const hobbiesStore = useHobbiesStore();

hobbiesStore.fetchHobbies();

const newHobby = ref({ name: '', description: '' });
const showAddHobbyModal = ref(false);

const handleAddHobby = async () => {
  if (newHobby.value.name.trim() === '') {
    alert('Hobby name is required.');
    return;
  }
  
  await hobbiesStore.addHobby(newHobby.value); 
  newHobby.value = { name: '', description: '' }; 
  showAddHobbyModal.value = false; 
};

const closeModal = () => {
  showAddHobbyModal.value = false;
};

const handleDeleteHobby = async (id: number) => {
  await hobbiesStore.deleteHobby(id);
}

</script>

<style scoped>
.table {
  width: 100%;
  margin: 20px auto;
  border-collapse: separate;
  border-spacing: 0;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
}

.table thead {
  background-color: #f2f2f2;
  text-transform: uppercase;
  font-weight: bold;
}

.table thead th {
  padding: 15px;
  text-align: left;
  color: #333;
}

.table tbody tr:nth-child(odd) {
  background-color: #fafafa;
}

.table tbody tr:hover {
  background-color: #f5f5f5;
  transition: background-color 0.3s ease;
}

.table tbody td {
  padding: 12px 15px;
  font-size: 15px;
  color: #444;
  vertical-align: middle;
}

.table tbody .btn-danger {
  font-size: 14px;
  padding: 5px 10px;
}

/* Modal Styling */
.modal {
  background-color: rgba(0, 0, 0, 0.6);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
}

.modal-dialog {
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  width: 90%;
  max-width: 500px;
  padding: 20px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
  font-weight: bold;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
}

.modal-header .btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #888;
  cursor: pointer;
}

.modal-header .btn-close:hover {
  color: #555;
}

.modal-body {
  padding: 20px 0;
}

.modal-label {
  font-weight: bold;
  margin-bottom: 5px;
}

.form-control {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  width: 100%;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  border-top: 1px solid #ddd;
  padding-top: 10px;
}

.modal-footer .btn {
  margin-left: 10px;
}

.modal-footer .btn-secondary {
  background-color: #ccc;
  color: #333;
  border: none;
}

.modal-footer .btn-secondary:hover {
  background-color: #bbb;
}

.modal-footer .btn-primary {
  background-color: #007bff;
  color: #fff;
  border: none;
}

.modal-footer .btn-primary:hover {
  background-color: #0056b3;
}

/* Button Styling */
.btn {
  border-radius: 5px;
  font-size: 14px;
  padding: 8px 15px;
}

.btn-primary {
  background-color: #007bff;
  color: white;
  border: none;
  transition: background-color 0.3s ease;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
  border: none;
  transition: background-color 0.3s ease;
}

.btn-danger:hover {
  background-color: #a71d2a;
}

/* Responsive Design */
@media (max-width: 768px) {
  .table tbody td,
  .table thead th {
    font-size: 14px;
  }

  .btn {
    font-size: 12px;
  }

  .modal-dialog {
    width: 95%;
  }
}
</style>