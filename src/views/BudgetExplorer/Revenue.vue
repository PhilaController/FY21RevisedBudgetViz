<template>
  <BudgetExplorer
    label="revenue"
    vizClass="revenue-explorer"
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
      annotationLabels: ["Revenue increases", "Revenue decreases"],
      viewingOptions: ["All Changes", "By Revenue Source"],
      tableConfig: {
        grouped: ["By Revenue Source"],
        groupby: {
          "All Changes": "name",
          "By Revenue Source": "revenue_source"
        },
        childColumns: {},
        headerColumns: [
          {
            label: "Name",
            field: "name",
            required: true
          },
          {
            label: "Revenue Source",
            field: "revenue_source",
            required: true
          }
        ]
      },
      rawData: require("@/data/revenue_revisions.json")
    };
  },
  computed: {
    legendConfig() {
      return {
        sizes: !this.smallScreen ? [1e6, 50e6, 200e6] : [1e6, 200e6],
        colorScaleDomain: [-0.3, 0.3],
        label: "projected revenues"
      };
    },
    viewingConfig() {
      return {
        "All Changes": {
          columns: 1,
          height: 250,
          force_type: "charge",
          force_strength: 0.1
        },
        "By Revenue Source": {
          columns: this.smallScreen ? 1 : 3,
          height: this.smallScreen ? 550 : 300,
          groupby: "revenue_source",
          force_type: "collide",
          force_strength: 0.05
        }
      };
    },
    smallScreen() {
      return window.screen.width <= 768;
    }
  }
};
</script>
