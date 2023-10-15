<template>
    <div class="p-3">
        <b-row class="justify-content-md-center py-3">
            <b-col col>
                <b-form-input v-model="filter" placeholder="Book Title"></b-form-input>
            </b-col>
            <b-col cols="12" md="auto">
                <b-button v-if="id" @click="addnew">
                    <!-- <b-icon icon="add"></b-icon> \ -->
                    Book
                </b-button>
            </b-col>
        </b-row>

        <div>
            <b-table
                v-if="dataList.length"
                striped
                hover
                :fields="fields"
                :items="dataList"
                :filter="filter"
                @filtered="onFiltered"
                @row-clicked="edit"
            ></b-table>
        </div>
        <!-- Generated random ID to prevent multiple modal from possible multiple component to clash -->
        <bookForm
            v-if="id"
            :id="id"
            :ref="id"
            :currentAuthor="currentAuthor"
            @updateSucceed="updateSucceed"
            @updateFailed="updateFailed"
            @createSucceed="createSucceed"
            @createFailed="createFailed"
            @deleteSucceed="deleteSucceed"
            @deleteFailed="deleteFailed"
        ></bookForm>
    </div>
</template>
<script>
import bookForm from '@/components/bookForm';
import * as crud from '@/api/crud.js';
import fn from '@/helper/functions';

export default {
    props: ['currentAuthor', 'currentBook'],
    watch: {},
    components: {
        bookForm,
    },
    data() {
        return {
            id: null,
            filter: '',
            fields: [
                {
                    key: 'id',
                    label: 'ID',

                    sortable: true,
                },
                {
                    key: 'author',
                    formatter: (val) => val?.name,
                    sortable: false,
                },
                {
                    key: 'title',
                    sortable: false,
                },
                {
                    key: 'num_pages',
                    label: 'Page count',
                    sortable: true,
                },
            ],
            fields2: [
                {
                    key: 'id',
                    label: 'ID',

                    sortable: true,
                },
                {
                    key: 'title',
                    sortable: false,
                },
                {
                    key: 'num_pages',
                    label: 'Page count',
                    sortable: true,
                },
            ],
            dataList: [],
            // define the default value
            value: null,
            // define options
            totalRows: 0,
            currentPage: 1,
        };
    },
    methods: {
        async getdata() {
            this.dataList = await crud.getAll(this.$axios, 'book', {});
        },
        addnew() {
            this.$refs[this.id]?.addnew();
        },
        edit(item, index) {
            this.$refs[this.id]?.edit({ ...item });
        },
        updateSucceed(newdata) {
            console.log(newdata);
        },
        updateFailed() {
            console.log('Update data Failed');
        },
        createSucceed(newdata) {
            this.dataList.push(newdata);
            console.log(newdata);
        },
        createFailed() {
            console.log('Register author Failed');
        },
        deleteSucceed(newdata) {
            // this.dataList.push(newdata);
            console.log(newdata);
        },
        deleteFailed() {
            console.log('delete author Failed');
        },
        onFiltered(filteredItems) {
            // Trigger pagination to update the number of buttons/pages due to filtering
            this.totalRows = filteredItems.length;
            this.currentPage = 1;
        },
    },
    created() {
        if (this.currentBook) {
            this.dataList = this.currentBook;
            this.fields = this.fields2;
        } else this.getdata();
        this.id = fn.fn.random();
    },
};
</script>
