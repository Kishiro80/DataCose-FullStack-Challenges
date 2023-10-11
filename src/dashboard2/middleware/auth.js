export default function ({ app, route, redirect }) {
    // console.log(route, redirect);
    const isAuthenticated = app.$auth.loggedIn;

    if (!isAuthenticated) {
        // console.log('not auth');
        if (!route.meta.noAuth) {
            // console.log('go  login');
            return redirect('/login'); // Redirect to the login page if not authenticated
        }
    }
}
