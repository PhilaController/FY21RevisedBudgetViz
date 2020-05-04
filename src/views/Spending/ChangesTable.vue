<template></template>

<script>
import { group } from "d3-array";
import "vue-good-table/dist/vue-good-table.css";
import { VueGoodTable } from "vue-good-table";

export default {
  components: {
    "vue-good-table": VueGoodTable
  },
  props: ["rawData", "groupby"],
  data() {
    return {
      rows: [
        {
          id: 0,
          name: "Senior Devs",
          score: 0.15296,
          children: [
            { id: 1, name: "John", age: 20, score: 0.03845 },
            { id: 2, name: "Jane", age: 24, score: 0.02948 },
            { id: 3, name: "Susan", age: 16, score: 0.08503 }
          ]
        },
        {
          id: 4,
          name: "Junior Devs",
          score: 0.12069,
          children: [
            { id: 5, name: "Chris", age: 55, score: 0.02946 },
            { id: 6, name: "Dan", age: 40, score: 0.09123 }
          ]
        }
      ]
    };
  },
  mounted() {
    console.log(this.formattedData);
  },
  computed: {
    columns() {
      return [
        {
          label: "Name",
          field: "name"
        },
        {
          label: "Proposed",
          field: `${this.fiscalYear} (Proposed)`,
          type: "number"
        },
        {
          label: "Revised",
          field: `${this.fiscalYear} (Revised)`,
          type: "number"
        },
        {
          label: "Dollar Change",
          field: "diff",
          type: "number"
        },
        {
          label: "Percent Change",
          field: "percent_diff",
          type: "percentage"
        }
      ];
    },
    formattedData() {
      let out = [];
      return group(this.rawData, d => d.dept_name);
      //   console.log(grouped);
    }
  }
};
</script>

<style>
</style>