<template>
    <b-container class="justify-content-md-center" align-v="center">
        <b-card title="System Login" header-tag="header" footer-tag="footer">
            <template #header>
                <h6 class="mb-0">Book Archive, Digitalized.</h6>
            </template>
            <b-card-body>
                <b-form @submit="login">
                    <b-form-group label="Username" label-for="Username">
                        <b-form-input id="Username" v-model="form.username" type="text" required> </b-form-input>
                    </b-form-group>
                    <b-form-group label="Password" label-for="password">
                        <b-form-input id="password" v-model="form.password" type="password" required> </b-form-input>
                    </b-form-group>
                    <b-button type="submit" variant="primary">Login</b-button>
                </b-form>
            </b-card-body>
            <template #footer>
                <em>© 2023 DataCose.com</em>
            </template>
        </b-card>
    </b-container>
</template>

<script>
export default {
    data() {
        return {
            form: {
                username: null,
                password: null,
            },
        };
    },
    methods: {
        async login(event) {
            event.preventDefault(); // Prevent the default form submission behavior

            console.log('logging in');
            try {
                const formData = new FormData();
                formData.append('username', this.form.username);
                formData.append('password', this.form.password);
                console.log('res');

                let res = await this.$auth.loginWith('local', {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                    data: formData,
                });
                console.log('res', res);
                this.$router.push('/Author');
            } catch (error) {
                console.error(error);
            }
        },
    },
};
</script>
