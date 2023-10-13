<template>
  <div>
    <h1>Error</h1>
    <p>Page not found. Redirecting...</p>
  </div>
</template>

<script>
export default {
  async asyncData({ error }) {
    if (error.statusCode === 404) {
      // Redirect to your desired URL
      return {
        redirectUrl: "/your-redirect-url",
      };
    }
  },
  async mounted() {
    if (this.redirectUrl) {
      // Perform the automatic redirection
      this.$router.push(this.redirectUrl);
    }
  },
};
</script>
