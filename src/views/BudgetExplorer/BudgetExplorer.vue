<template>
  <!-- Outside wrapper -->
  <div class="budget-explorer-container">
    <!-- User Toolbar -->
    <div class="title d-flex justify-content-center">
      <div>
        Revised {{ label }} for the fiscal year&nbsp;
        <!-- Year Selection -->
        <Dropdown
          class="title-dropdown"
          ref="fiscalYearDropdown"
          :options="fiscalYearOptions"
          :defaultValue="fiscalYear"
          @change="updateYearDropdown($event, 'fiscalYear')"
        />&nbsp;budget
      </div>
    </div>

    <!-- The total change -->
    <div class="total-change text-center mt-3 pb-3">{{ formattedTotalChange }}</div>

    <!-- Radio toolbar for different views -->
    <div class="budget-explorer-toolbar d-flex align-items-center justify-content-center mt-3">
      <RadioButtonToolbar
        :options="viewingOptions"
        :defaultValue="selectedViewingOption"
        ref="viewingOptionsToolbar"
        @change="setViewingOption"
      />
    </div>

    <!-- Budget Explorer Viz -->
    <BudgetExplorerViz
      class="mt-5"
      :width="totalWidth"
      :fiscalYear="fiscalYear"
      :rawData="rawData"
      :viewingMode="selectedViewingOption"
      :viewingConfig="viewingConfig"
      :tableConfig="tableConfig"
      :legendConfig="legendConfig"
      :annotationLabels="annotationLabels"
      :vizClass="vizClass"
    />
  </div>
</template>

<script>
import * as d3 from "d3";
import Dropdown from "./Dropdown";
import RadioButtonToolbar from "./RadioButtonToolbar";
import BudgetExplorerViz from "./BudgetExplorerViz";
import { netChangeFormatFn } from "@/utils/formatFns";

// Years to show
const YEARS = [2020, 2021, 2022, 2023, 2024, 2025];

export default {
  components: { Dropdown, RadioButtonToolbar, BudgetExplorerViz },
  props: [
    "label",
    "rawData",
    "tableConfig",
    "legendConfig",
    "viewingConfig",
    "viewingOptions",
    "annotationLabels",
    "vizClass"
  ],
  data() {
    return {
      fiscalYearOptions: YEARS,
      selectedViewingOption: this.viewingOptions[0],
      fiscalYear: 2021
    };
  },
  mounted() {
    this.updateTotalChangeColor();
  },
  methods: {
    updateTotalChangeColor() {
      // Green or red?
      if (this.totalChange > 0) {
        $(".total-change")
          .addClass("green")
          .removeClass("red");
      } else {
        $(".total-change")
          .addClass("red")
          .removeClass("green");
      }
    },
    setViewingOption(value) {
      this.selectedViewingOption = value;
    },
    updateYearDropdown(selectedYear, tag) {
      this.fiscalYear = selectedYear;
      this.updateTotalChangeColor();
    }
  },
  computed: {
    totalWidth() {
      return Math.min(window.screen.width * 0.9, 1000);
    },
    formattedTotalChange() {
      return netChangeFormatFn(this.totalChange);
    },
    totalChange() {
      let out = 0,
        row;
      for (let i = 0; i < this.rawData.length; i++) {
        row = this.rawData[i];
        out +=
          row[`${this.fiscalYear} (Revised)`] -
          row[`${this.fiscalYear} (Proposed)`];
      }
      return out;
    }
  }
};
</script>

<style>
.title {
  font-weight: 700;
  font-size: 1.7rem;
}
.title-dropdown > button {
  font-size: 1.7rem;
  background-color: white;
  color: #2176d2 !important;
  margin-bottom: 0.5rem;
  border-color: #2176d2;
  padding-bottom: 0px;
  padding-top: 0px;
}
.title-dropdown .dropdown-item {
  font-size: 1.7rem;
  font-weight: 300;
}
.title-dropdown > button:hover,
.title-dropdown > button:focus {
  background-color: #2176d2 !important;
  color: #fff !important;
  margin-bottom: 0.5rem;
  border-color: #2176d2;
}
.total-change {
  font-size: 2.5rem;
  font-weight: 700;
  border-bottom: 2px solid #deedfc;
}
.green {
  color: #398649;
}
.red {
  color: #da3b46;
}
</style>