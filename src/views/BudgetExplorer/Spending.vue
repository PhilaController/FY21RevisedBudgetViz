<template>
  <BudgetExplorer
    label="spending"
    vizClass="spending-explorer"
    :rawData="rawData"
    :viewingOptions="viewingOptions"
    :viewingConfig="viewingConfig"
    :tableConfig="tableConfig"
    :legendConfig="legendConfig"
    :annotationLabels="annotationLabels"
  />
</template>

<script>
import BudgetExplorer from "./BudgetExplorer";
import { percentFn, netChangeFormatFn, formatFn } from "@/utils/formatFns";

export default {
  components: { BudgetExplorer },
  data() {
    return {
      annotationLabels: ["Budget increases", "Budget cuts"],
      viewingOptions: [
        "All Changes",
        "By Department",
        "By Major Class",
        "By Category"
      ],
      tableConfig: {
        grouped: [
          "All Changes",
          "By Department",
          "By Major Class",
          "By Category"
        ],
        groupby: {
          "All Changes": "name",
          "By Department": "name",
          "By Major Class": "major_class_description",
          "By Category": "category_code_description"
        },
        childColumns: {},
        headerColumns: [
          {
            label: "Name",
            field: "name",
            required: true
          },
          {
            label: "Major Class",
            field: "major_class_description",
            required: true
          },
          {
            label: "Category",
            field: "category_code_description",
            required: false
          }
        ]
      },
      rawData: require("@/data/budget_revisions_by_major_class.json")
    };
  },
  computed: {
    smallScreen() {
      return window.screen.width <= 768;
    },
    legendConfig() {
      return {
        sizes: this.smallScreen ? [1e6, 50e6] : [1e6, 10e6, 50e6],
        colorScaleDomain: [-1, 1],
        label: "budgeted spending"
      };
    },
    viewingConfig() {
      return {
        "All Changes": {
          columns: 1,
          height: 400,
          force_type: "charge",
          force_strength: 0.3
        },
        "By Department": {
          columns: this.smallScreen ? 2 : 4,
          height: this.smallScreen ? 3500 : 2500,
          groupby: "dept_name",
          force_type: "collide",
          force_strength: 0.05
        },
        "By Major Class": {
          columns: this.smallScreen ? 2 : 3,
          height: this.smallScreen ? 750 : 650,
          groupby: "major_class_description",
          force_type: "collide",
          force_strength: 0.05
        },
        "By Category": {
          columns: this.smallScreen ? 2 : 4,
          height: this.smallScreen ? 1000 : 800,
          groupby: "category_code_description",
          force_type: "collide",
          force_strength: 0.05
        }
      };
    }
  }
};
</script>
