<template>
  <b-modal :id="id">
    <template #modal-header="{ close }">
      <!-- Emulate built in modal header close button action -->
      <h5>
        {{ modeEdit ? "Edit" : "Create" }} Book {{ data.id ? `#${data.id}` : null }}
      </h5>
      <b-button size="sm" variant="outline-danger" @click="close()"> X </b-button>
    </template>

    <template #default>
      <b-form @submit="save">
        <b-form-group
          id="input-group-1"
          label="Book Title:"
          label-for="input-1"
          description="Book Title?"
        >
          <b-form-input
            id="input-1"
            name="input-1"
            v-model="data.title"
            type="text"
            placeholder="The Triology"
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          id="input-group-2"
          label="Pages count:"
          label-for="input-2"
          description="How many pages does it have?"
        >
          <b-form-input
            id="input-2"
            name="input-2"
            v-model="data.num_pages"
            type="number"
            placeholder="10"
            required
          ></b-form-input>
        </b-form-group>
      </b-form>

      <treeselect
        id="author"
        name="author"
        v-model="data.author"
        valueFormat="object"
        :options="authorList"
        :normalizer="normalizer"
      >
        <div slot="value-label" slot-scope="{ node }">{{ node.raw.name }}</div>
      </treeselect>
    </template>

    <template #modal-footer>
      <b-button size="sm" variant="success" @click="save"> Save </b-button>
      <b-button size="sm" variant="warning" @click="resetData"> Reset </b-button>
      <b-button v-if="modeEdit" size="sm" variant="danger" @click="deleteOne">
        Delete
      </b-button>
    </template>
  </b-modal>
</template>
<script>
import Treeselect from "@riophae/vue-treeselect";

import fn from "@/helper/functions";
import * as crud from "@/api/crud.js";

export default {
  props: ["id", "currentAuthor"],
  emits: [
    "createSucceed",
    "createFailed",
    "updateSucceed",
    "updateFailed",
    "deleteSucceed",
    "deleteFailed",
  ],
  components: { Treeselect },

  data() {
    return {
      root: "book",
      value: null,

      data: {
        id: null,
        title: null,
        num_pages: 0,
        author: null,
      },
      originalData: {
        id: null,
        title: null,
        num_pages: 0,
        author: null,
      },
      emptyData: {
        id: null,
        title: null,
        num_pages: 0,
        author: null,
      },
      authorList: [],
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
      console.log(data, "setdata bookform");
      this.originalData = fn.fn.deepCopy({ ...data });
      this.data = fn.fn.deepCopy({ ...this.originalData });
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
      console.log("saving?");
      let data = { ...this.data };
      data.author_id = data.author_id ? data.author_id : data.author.id;
      const { author, ...cleandata } = data;

      if (this.modeEdit) {
        crud
          .update(this.$axios, this.root, this.data.id, cleandata)
          .then((res) => {
            res.author = author;
            this.$emit("updateSucceed", res);
            this.closeModal();
          })
          .catch((error) => {
            console.error("The Promise is rejected!", error);

            this.$emit("updateFailed");
          });
      } else {
        crud
          .create(this.$axios, this.root, cleandata)
          .then((res) => {
            res.author = author;
            this.$emit("createSucceed", res);
            this.closeModal();
          })
          .catch((error) => {
            console.error("The Promise is rejected!", error);

            this.$emit("createFailed");
          });
      }
    },
    async deleteOne() {
      crud
        .deleteOne(this.$axios, this.root, this.data.id)
        .then((res) => {
          this.$emit("deleteSucceed", this.data);
          this.closeModal();
        })
        .catch((error) => {
          console.error("The Promise is rejected!", error);

          this.$emit("deleteFailed");
        });
    },
    getauthorlist() {
      crud.getAll(this.$axios, "author", {}).then((res) => {
        this.authorList = res;
      });
    },
    normalizer(node) {
      return {
        id: node.id,
        label: node.name,
      };
    },
  },
  created() {
    if (this.currentAuthor) {
      this.authorList = [this.currentAuthor];
      this.data.author = this.currentAuthor;
    } else this.getauthorlist();
    console.log(fn);
  },
};
</script>
