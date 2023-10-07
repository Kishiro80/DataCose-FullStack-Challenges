<template>
  <div>
    <div>
      THis is normal link
      <NuxtLink to="/"> About (internal link that belongs to the Nuxt App) </NuxtLink>
    </div>
    <div>
      <template v-for="(item, index) in items"> {{ item }}</template>
    </div>
  </div>
</template>
<script>
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
  layout: "blog",
};
</script>
