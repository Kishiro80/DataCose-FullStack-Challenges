export default function ({ app, route, redirect }) {
    const isAuthenticated = true; // app.$auth.loggedIn;

    if (!isAuthenticated) {
        if (!route.meta.noAuth) {
            return redirect('/login'); // Redirect to the login page if not authenticated
        }
    }
}
