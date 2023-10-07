<template>
  <div>
    <div>
      THis is normal link
      <NuxtLink to="/"> About (internal link that belongs to the Nuxt App) </NuxtLink>
    </div>
    <div></div>
  </div>
</template>
<script setup>
import { ref } from "vue";

export default {
  setup() {
    const items = ref(["😏", "😐", "😑", "😒", "😕"]);
    function removeItem(toRemove) {
      items.value = items.value.filter((item) => item !== toRemove);
    }
    return {
      removeItem,
      items,
    };
  },
};
</script>
