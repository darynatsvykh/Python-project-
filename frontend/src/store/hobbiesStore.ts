import { defineStore } from "pinia";

interface Hobby {
    id: number;
    name: string;
    description: string;
}

interface NewHobby {
    name: string;
    description?: string;
}

export const useHobbiesStore = defineStore('hobbies', {
    state: () => ({
      hobbies: [] as Hobby[], 
    }),
  
    actions: {
      async fetchHobbies() {
        try {
          const response = await fetch('http://127.0.0.1:8000/hobbies/');
          if (!response.ok) {
            throw new Error(`Error fetching hobbies: ${response.status}`);
          }
          const data = await response.json();
          this.hobbies = data.Hobbies; 
        } catch (error) {
          console.error(error);
        }
      },
  
      async addHobby(newHobby: NewHobby) {
        try {

          const response = await fetch('http://127.0.0.1:8000/hobbies/add/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(newHobby),
          });
          if (!response.ok) {
            throw new Error(`Error adding hobby: ${response.status}`);
          }
          await this.fetchHobbies(); 
        } catch (error) {
          console.error(error);
        }
      },

      async deleteHobby(hobbyId: number) {

        const response = await fetch(`http://127.0.0.1:8000/hobbies/delete/${hobbyId}/`, {
            method: 'DELETE',
            headers:{
              'Content-Type': 'application/json',
            }
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to delete hobby');
        }
        this.hobbies = this.hobbies.filter(hobby => hobby.id !== hobbyId);
     },
    },
  });

