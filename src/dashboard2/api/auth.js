export default function ({ $axios }) {
    $axios.onError((error) => {
        if (error.response.status === 401) {
            this.$auth.logout();
        }
        return Promise.reject(error);
    });
}
