<template>
    <b-modal :id="id">
        <template #modal-header="{ close }">
            <!-- Emulate built in modal header close button action -->
            <h5>{{ modeEdit ? 'Edit' : 'Create' }} Author {{ data.id ? `#${data.id}` : null }}</h5>
            <b-button size="sm" variant="outline-danger" @click="close()"> X </b-button>
        </template>

        <template #default>
            <b-form @submit="save">
                <b-form-group
                    id="input-group-1"
                    label="Author Name:"
                    label-for="input-1"
                    description="Who is the author?"
                >
                    <b-form-input
                        id="input-1"
                        v-model="data.name"
                        type="text"
                        placeholder="Conan Doyle"
                        required
                    ></b-form-input>
                </b-form-group>
            </b-form>
            <bookComponent :currentBook="data.book" :currentAuthor="data"></bookComponent>
        </template>

        <template #modal-footer>
            <b-button size="sm" variant="success" @click="save"> Save </b-button>
            <b-button size="sm" variant="warning" @click="resetData"> Reset </b-button>
            <b-button v-if="modeEdit" size="sm" variant="danger" @click="deleteOne"> Delete </b-button>
        </template>
    </b-modal>
</template>
<script>
import fn from '@/helper/functions';
import * as crud from '@/api/crud.js';
import bookComponent from '@/components/bookComponent';

export default {
    props: ['id'],
    emits: ['createSucceed', 'createFailed', 'updateSucceed', 'updateFailed', 'deleteSucceed', 'deleteFailed'],

    components: {
        bookComponent,
    },

    data() {
        return {
            root: 'author',
            filter: null,
            totalRows: 0,
            currentPage: 1,
            data: {
                id: null,
                name: null,
                bookCount: 0,
            },
            originalData: {
                id: null,
                name: null,
                bookCount: 0,
            },
            emptyData: {
                id: null,
                name: null,
                bookCount: 0,
            },
        };
    },

    computed: {
        modeEdit() {
            return this.data?.id ? true : false;
        },
    },
    methods: {
        openModal() {
            this.$bvModal.show(this.id);
        },
        closeModal() {
            this.$bvModal.hide(this.id);
        },
        cleardata() {
            this.data = this.emptyData;
        },
        setData(data) {
            this.originalData = fn.fn.deepCopy(data);
            this.data = fn.fn.deepCopy(this.originalData);
        },
        resetData(data) {
            this.data = fn.fn.deepCopy(this.originalData);
        },
        addnew(data = {}) {
            this.setData({ ...this.emptyData, ...data });
            this.openModal();
        },
        edit(input) {
            this.setData(input);
            this.openModal();
        },
        async save() {
            if (this.modeEdit) {
                crud.update(this.$axios, this.root, this.data.id, this.data)
                    .then((res) => {
                        this.$emit('updateSucceed', res);
                        this.closeModal();
                    })
                    .catch((error) => {
                        console.error('The Promise is rejected!', error);

                        this.$emit('updateFailed');
                    });
            } else {
                crud.create(this.$axios, this.root, this.data)
                    .then((res) => {
                        this.$emit('createSucceed', res);
                        this.closeModal();
                    })
                    .catch((error) => {
                        console.error('The Promise is rejected!', error);

                        this.$emit('createFailed');
                    });
            }
        },
        async deleteOne() {
            crud.deleteOne(this.$axios, this.root, this.data.id)
                .then((res) => {
                    this.$emit('deleteSucceed', res);
                    this.closeModal();
                })
                .catch((error) => {
                    console.error('The Promise is rejected!', error);

                    this.$emit('deleteFailed');
                });
        },
        onFiltered(filteredItems) {
            // Trigger pagination to update the number of buttons/pages due to filtering
            this.totalRows = filteredItems.length;
            this.currentPage = 1;
        },
    },
    created() {
        console.log(fn);
    },
};
</script>
