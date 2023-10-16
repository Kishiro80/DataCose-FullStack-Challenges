<template>
  <div class="p-3">
    <b-row class="justify-content-md-center py-3">
      <b-col col>
        <b-form-input v-model="filter" placeholder="Book Title"></b-form-input>
      </b-col>
      <b-col cols="12" md="auto">
        <b-button v-if="id" @click="addnew">
          <!-- <b-icon icon="add"></b-icon> \ -->
          Add Book
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
import bookForm from "@/components/bookForm";
import * as crud from "@/api/crud.js";
import fn from "@/helper/functions";

export default {
  props: ["currentAuthor", "currentBook"],
  emits: ["createSucceed", "deleteSucceed"],
  components: {
    bookForm,
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
          key: "author",
          formatter: (val) => val?.name,
          sortable: false,
        },
        {
          key: "title",
          sortable: false,
        },
        {
          key: "num_pages",
          label: "Page count",
          sortable: true,
        },
      ],
      fields2: [
        {
          key: "id",
          label: "ID",

          sortable: true,
        },
        {
          key: "title",
          sortable: false,
        },
        {
          key: "num_pages",
          label: "Page count",
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
      this.dataList = await crud.getAll(this.$axios, "book", {});
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
      const authorWithoutBooks = {
        id: newdata.author.id,
        name: newdata.author.name,
        book_count: newdata.author.book_count,
      };

      // Create the final data object with the author information and bookinfo
      const data = {
        author: authorWithoutBooks,
        num_pages: newdata.num_pages,
        title: newdata.title,
        author_id: newdata.author_id,
        id: newdata.id,
      };

      // Push the data to the dataList
      this.dataList.push(data);
      this.$emit("createSucceed");

      console.log(data, "bookform update data");
    },
    createFailed() {
      console.log("Register author Failed");
    },
    deleteSucceed(deletedData) {
      // this.dataList.push(newdata);
      this.dataList = this.dataList.filter((item) => item.id !== deletedData.id);

      this.$emit("deleteSucceed");
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
    if (this.currentBook) {
      this.dataList = this.currentBook;
      this.fields = this.fields2;
    } else this.getdata();
    this.id = fn.fn.random();
  },
};
</script>
