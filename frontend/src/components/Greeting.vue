<template>
    <div class="greeting">
      <h2>Welcome back, {{ username }}!</h2>
      <p>We're glad to see you again.</p>
    </div>
</template>
  
<script lang="ts">
  import { defineComponent, ref, onMounted } from "vue";
  
  export default defineComponent({
    name: "Greeting",
    setup() {
      const username = ref<string | null>("");

      onMounted(() => {
        const storedUsername = localStorage.getItem("username");
        if (storedUsername) {
          username.value = storedUsername;
        } else {
          username.value = null;
        }
      });
  
      return { username };
    },
  });
 </script>
  
<style scoped>
  .greeting {
    text-align: center;
    background: linear-gradient(135deg, #f9f9f9, #e4e7eb);
    padding: 30px;
    margin: 20px auto;
    border: 1px solid #ccc;
    border-radius: 12px;
    max-width: 600px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, background-color 0.3s ease;
  }
  
  .greeting:hover {
    transform: translateY(-5px);
    background: linear-gradient(135deg, #e4e7eb, #f9f9f9);
  }
  
  .greeting h2 {
    font-size: 26px;
    color: #343a40;
    font-family: "Arial", sans-serif;
    margin-bottom: 15px;
    font-weight: bold;
    letter-spacing: 1px;
    text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.1);
  }
  
  .greeting p {
    font-size: 18px;
    color: #63686e;
    font-family: "Roboto", sans-serif;
    margin-top: 10px;
    line-height: 1.6;
  }
</style>