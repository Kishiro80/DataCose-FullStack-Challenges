export default {
    // Disable server-side rendering: https://go.nuxtjs.dev/ssr-mode
    ssr: false,

    // Target: https://go.nuxtjs.dev/config-target
    target: 'static',
    router: {
        middleware: ['auth'], // Apply the 'auth' middleware to all routes
    }, // Global page headers: https://go.nuxtjs.dev/config-head
    loading: {
        color: 'blue',
        height: '5px',
    },
    head: {
        title: 'DC Full Stack Code Challenge',
        htmlAttrs: {
            lang: 'en',
        },
        meta: [
            { charset: 'utf-8' },
            {
                name: 'viewport',
                content: 'width=device-width, initial-scale=1',
            },
            { hid: 'description', name: 'description', content: '' },
            { name: 'format-detection', content: 'telephone=no' },
        ],
        link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
    },

    // Global CSS: https://go.nuxtjs.dev/config-css
    css: [],

    // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
    plugins: [],

    // Auto import components: https://go.nuxtjs.dev/config-components
    components: true,

    // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
    buildModules: [
        // https://go.nuxtjs.dev/typescript
        '@nuxt/typescript-build',
    ],

    // Modules: https://go.nuxtjs.dev/config-modules
    modules: [
        // https://go.nuxtjs.dev/bootstrap
        // https://go.nuxtjs.dev/axios
        '@nuxtjs/axios',
        '@nuxtjs/auth',
        '@nuxtjs/bootstrap-vue',
    ],

    // Axios module configuration: https://go.nuxtjs.dev/config-axios
    axios: {
        // Workaround to avoid enforcing hard-coded localhost:3000: https://github.com/nuxt-community/axios-module/issues/308
        baseURL: process.env.NODE_ENV == 'development' ? 'http://127.0.0.1:8000' : process.env.BASEURL,
    },

    // Build Configuration: https://go.nuxtjs.dev/config-build
    build: {},
    auth: {
        strategies: {
            local: {
                endpoints: {
                    login: { url: '/auth/login', method: 'post', propertyName: 'access_token' },
                    logout: { url: '/auth/logout', method: 'post' },
                    user: { url: '/auth/users/me', method: 'get', propertyName: 'user' },
                },
                tokenRequired: true,
                tokenType: 'Bearer',
            },
        },
        redirect: {
            login: '/login',
            logout: '/login',
            callback: '/login',
            home: '/',
        },
    },

    generate: {
        fallback: true,
    },

    // Define the custom error page
    generate: {
        fallback: 'custom-404',
    },
};
