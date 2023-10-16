<template>
  <div class="p-3">
    <h1>Author Page</h1>
    <b-row class="justify-content-md-center py-3">
      <b-col col>
        <b-form-input v-model="filter" placeholder="Enter Author Name"></b-form-input>
      </b-col>
      <b-col cols="12" md="auto">
        <b-button v-if="id" @click="addnew"> Add Author </b-button>
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
    <authorForm
      v-if="id"
      :id="id"
      :ref="id"
      @updateSucceed="updateSucceed"
      @updateFailed="updateFailed"
      @createSucceed="createSucceed"
      @createFailed="createFailed"
      @deleteSucceed="deleteSucceed"
      @deleteFailed="deleteFailed"
    ></authorForm>
  </div>
</template>
<script>
import Treeselect from "@riophae/vue-treeselect";
import authorForm from "@/components/authorForm";
import * as crud from "@/api/crud.js";
import fn from "@/helper/functions";

export default {
  watch: {},
  layout: "ProtectedContent",
  components: {
    Treeselect,
    authorForm,
  },
  data() {
    return {
      id: null,
      filter: "",
      fields: [
        {
          key: "id",
          label: "ID",

          sortable: true,
        },
        {
          key: "name",
          sortable: false,
        },
        {
          key: "book_count",
          sortable: true,

          label: "Book Count",
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
      this.dataList = await crud.getAll(this.$axios, "author", {}, "bookCount/");
    },
    addnew() {
      this.$refs[this.id]?.addnew();
    },
    edit(item, index) {
      this.$refs[this.id]?.edit({ ...item });
    },
    updateSucceed(updatedData) {
      this.dataList = this.dataList.map((item) => {
        if (item.id === updatedData.id) {
          return { ...item, ...updatedData };
        } else {
          return item;
        }
      });

      console.log("Update succeeded:", updatedData);
    },
    updateFailed() {
      console.log("Update data Failed");
    },
    createSucceed(newdata) {
      this.dataList.push(newdata);
      console.log(newdata);
    },
    createFailed() {
      console.log("Register author Failed");
    },
    deleteSucceed(deletedData) {
      // this.dataList.push(newdata);
      this.dataList = this.dataList.filter((item) => item.id !== deletedData.id);

      console.log(deletedData);
    },
    deleteFailed() {
      console.log("delete author Failed");
    },
    onFiltered(filteredItems) {
      // Trigger pagination to update the number of buttons/pages due to filtering
      this.totalRows = filteredItems.length;
      this.currentPage = 1;
    },
  },
  created() {
    this.getdata();
    this.id = fn.fn.random();
  },
};
</script>
