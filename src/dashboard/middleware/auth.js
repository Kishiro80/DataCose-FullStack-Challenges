export default function ({ route, redirect }) {
    if (!userIsAuthenticated()) {
        if (!route.meta.noAuth) {
            return redirect('/login'); // Redirect to the login page if not authenticated
        }
    }
}
