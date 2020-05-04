<template>
  <div class="d-flex justify-content-center">
    <VueApexCharts height="450" width="900" type="line" :options="chartOptions" :series="series"></VueApexCharts>
  </div>
</template>

<script>
import VueApexCharts from "vue-apexcharts";
import { format } from "d3-format";

export default {
  components: { VueApexCharts },
  data() {
    return {
      data: require("@/data/overtime_per_employee.json")
    };
  },
  computed: {
    chartOptions() {
      return {
        dataLabels: {
          enabled: false
        },
        chart: {
          toolbar: {
            show: false
          },
          zoom: { enabled: false }
        },
        grid: {
          padding: { left: 25, right: 25, bottom: -20 }
        },
        markers: {
          size: 7,
          strokeColor: "#cc3000",
          colors: ["#ffffff"],
          strokeWidth: 4
        },
        tooltip: {
          enabled: true,
          style: { fontSize: "20px" },
          y: {
            formatter: function(val) {
              return `$${format(".2f")(val)}k`;
            }
          }
        },
        xaxis: {
          type: "categories",
          categories: this.data["fiscal_year"],
          labels: {
            style: { fontSize: "20px" }
          },
          crosshairs: { show: false },
          min: 0,
          max: this.data["fiscal_year"].length + 1,
          tooltip: { enabled: false },
          title: {
            text: "Fiscal Year",
            style: {
              fontSize: "20px"
            }
          },
          axisTicks: { show: false }
        },
        yaxis: {
          labels: {
            style: {
              fontSize: "20px"
            },
            formatter: function(val) {
              return `$${format(".0f")(val)}k`;
            }
          },
          min: 5,
          forceNiceScale: true,
          crosshairs: { show: false }
        },

        colors: ["#cc3000"]
      };
    },
    series() {
      return [{ name: "", data: this.data["ot_per_employee"] }];
    }
  }
};
</script>



