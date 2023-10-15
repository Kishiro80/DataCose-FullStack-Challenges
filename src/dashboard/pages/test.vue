<template>
    <div>
        <div>
            <p>Testing Author API</p>
            <b-dropdown right text="author">
                <b-dropdown-item @click="AuthorgetOne">Get One</b-dropdown-item>
                <b-dropdown-item @click="AuthorgetAll">Get All</b-dropdown-item>
                <b-dropdown-item @click="Authorsearch">Search</b-dropdown-item>
                <b-dropdown-item @click="AuthorcreateOne">Create One</b-dropdown-item>
                <b-dropdown-item @click="AuthorupdateOne">Update One</b-dropdown-item>
                <b-dropdown-item @click="AuthordeleteOne">Delete One</b-dropdown-item>
            </b-dropdown>
            <b-dropdown right text="book">
                <b-dropdown-item @click="BookgetOne">Get One</b-dropdown-item>
                <b-dropdown-item @click="BookgetAll">Get All</b-dropdown-item>
                <b-dropdown-item @click="Booksearch">Search</b-dropdown-item>
                <b-dropdown-item @click="BookcreateOne">Create One</b-dropdown-item>
                <b-dropdown-item @click="BookupdateOne">Update One</b-dropdown-item>
                <b-dropdown-item @click="BookdeleteOne">Delete One</b-dropdown-item>
            </b-dropdown>
        </div>
        <div></div>
    </div>
</template>
<script>
import * as crud from '@/api/crud.js';
export default {
    layout: 'ProtectedContent',
    methods: {
        async AuthorgetOne() {
            const data = await crud.get(this.$axios, 'author', 1);
        },
        async AuthorgetAll() {
            const data = await crud.getAll(this.$axios, 'author', {});
        },
        async Authorsearch() {
            const data = await crud.search(this.$axios, 'author', {});
        },
        async AuthorcreateOne() {
            const data = await crud.create(this.$axios, 'author', { name: 'Conan Doyle' });
        },
        async AuthorupdateOne() {
            const data = await crud.update(this.$axios, 'author', 1, {});
        },
        async AuthordeleteOne() {
            const data = await crud.deleteOne(this.$axios, 'author', 1);
        },

        async BookgetOne() {
            const data = await crud.get(this.$axios, 'book', 1);
        },
        async BookgetAll() {
            const data = await crud.getAll(this.$axios, 'book', {});
        },
        async Booksearch() {
            const data = await crud.search(this.$axios, 'book', {});
        },
        async BookcreateOne() {
            const data = await crud.create(this.$axios, 'book', {
                title: 'bookOne',
                num_pages: 10,
                author_id: 1,
            });
        },
        async BookupdateOne() {
            const data = await crud.update(this.$axios, 'book', 1, {});
        },
        async BookdeleteOne() {
            const data = await crud.deleteOne(this.$axios, 'book', 1);
        },
    },
};
</script>
