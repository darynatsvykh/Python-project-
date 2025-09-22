<template>
  <div>
    <UsersTable />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import UsersTable from "../components/UsersTable.vue";

export default defineComponent({
  name: "MainPage",
  components: {
    UsersTable,
  },
});
</script>
