<template>
    <div>
        <nav v-if="$auth.loggedIn">
            <b-navbar toggleable="lg" type="dark" variant="dark">
                <b-navbar-brand href="#">My Book App</b-navbar-brand>
                <b-navbar-toggle target="nav-collapse"> </b-navbar-toggle>
                <b-collapse id="nav-collapse" is-nav>
                    <b-navbar-nav>
                        <b-nav-item v-for="(navItem, navIndex) in navList" :key="navIndex" :href="navItem.link">
                            {{ navItem.name }}
                        </b-nav-item>
                    </b-navbar-nav>
                    <b-navbar-nav class="ml-auto">
                        <b-nav-item-dropdown right>
                            <template v-slot:button-content>
                                <em>{{ $auth.user.name }}</em>
                            </template>
                            <b-dropdown-item @click="logout">Logout</b-dropdown-item>
                        </b-nav-item-dropdown>
                    </b-navbar-nav>
                </b-collapse>
            </b-navbar>
        </nav>
        <Nuxt />
    </div>
</template>
<script>
let navlist = [
    { link: '/Author', name: 'Author' },
    { link: '/Book', name: 'Book' },
];
export default {
    auth: true,
    data() {
        return {
            navList: navlist,
        };
    },
    methods: {
        async logout() {
            await this.$auth.logout();
            this.$router.push('/login');
        },
    },
};
</script>
