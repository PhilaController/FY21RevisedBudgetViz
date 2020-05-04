<template>
  <!-- Outside wrapper -->
  <div class="budget-explorer-container">
    <!-- User Toolbar -->
    <div class="title d-flex justify-content-center">
      <span>
        Revised revenues for the fiscal year&nbsp;
        <!-- Year Selection -->
        <Dropdown
          class="title-dropdown"
          ref="fiscalYearDropdown"
          :options="fiscalYearOptions"
          :defaultValue="fiscalYear"
          @change="updateYearDropdown($event, 'fiscalYear')"
        />&nbsp;budget
      </span>
    </div>
    <div class="total-change text-center">{{ netChangeFormatFn(totalChange) }}</div>
    <div class="budget-explorer-toolbar mt-3">
      <div class="d-flex align-items-center justify-content-center">
        <div class="radio-button-toolbar ml-5">
          <RadioButtonToolbar
            :options="viewingOptions"
            :defaultValue="selectedViewingOption"
            ref="viewingOptionsToolbar"
            @change="setViewingOption"
          />
        </div>
      </div>
    </div>

    <!-- Budget Explorer Viz -->
    <BudgetExplorerViz
      class="mt-5"
      :width="1000"
      :fiscalYear="fiscalYear"
      :viewingMode="selectedViewingOption"
      :rawData="rawData"
    />
  </div>
</template>

<script>
import * as d3 from "d3";
import Dropdown from "./Dropdown";
import RadioButtonToolbar from "./RadioButtonToolbar";
import BudgetExplorerViz from "./BudgetExplorerViz";

// Years to show
const YEARS = [2020, 2021, 2022, 2023, 2024, 2025];

export default {
  components: { Dropdown, RadioButtonToolbar, BudgetExplorerViz },
  data() {
    return {
      rawData: require("@/data/revenue_revisions.json"),
      fiscalYearOptions: YEARS,
      viewingOptions: ["All Changes", "By Revenue Source"],
      selectedViewingOption: "All Changes",
      fiscalYear: 2021
    };
  },
  mounted() {
    this.updateTotalChangeColor();
  },
  methods: {
    updateTotalChangeColor() {
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
    formatFn(d) {
      let s = `$${d3
        .format(",.3s")(Math.abs(d))
        .replace(/G/, "B")}`;
      if (d < 0) s = "\u2212" + s;
      return s;
    },
    netChangeFormatFn(d) {
      let s = this.formatFn(d);
      if (d > 0) s = "+" + s;
      return s;
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
  font-size: 2.2rem;
  font-weight: 700;
}
.green {
  color: #398649;
}
.red {
  color: #da3b46;
}
</style>