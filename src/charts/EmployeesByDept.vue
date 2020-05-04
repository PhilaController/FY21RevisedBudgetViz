<template>
  <div class="d-flex justify-content-center">
    <VueApexCharts height="450" width="900" :options="chartOptions" :series="series"></VueApexCharts>
  </div>
</template>

<script>
import VueApexCharts from "vue-apexcharts";
import { format } from "d3-format";

export default {
  components: { VueApexCharts },
  data() {
    return {
      data: require("@/data/employees_by_dept.json")
    };
  },
  computed: {
    chartOptions() {
      return {
        annotations: {
          position: "back",
          yaxis: [
            {
              y: 0,
              strokeDashArray: 0,
              borderColor: "#000",
              borderWidth: 3
            }
          ],
          xaxis: [
            {
              x: 0,
              strokeDashArray: 0,
              borderColor: "#000",
              borderWidth: 3
            }
          ]
        },
        dataLabels: {
          enabled: false
        },
        chart: {
          type: "scatter",
          zoom: {
            enabled: false
          },
          toolbar: {
            show: false
          }
        },
        grid: {
          padding: { left: 25, right: 25 }
        },
        // markers: {
        //   size: 7,
        //   strokeColor: "#666666",
        //   colors: ["#ffffff"],
        //   strokeWidth: 4
        // },
        tooltip: {
          enabled: true,
          style: { fontSize: "15px" },

          y: {
            formatter: function(val) {
              return `${format(",.0f")(val)}`;
            }
          }
        },
        xaxis: {
          tickAmount: 10,
          labels: {
            style: { fontSize: "20px" }
          },
          max: 300,
          min: -300,
          title: {
            text: "Change in Employees Since FY17",
            style: {
              fontSize: "20px"
            }
          },
          axisTicks: { show: false }
        },
        legend: {
          show: false
        },
        yaxis: {
          labels: {
            style: {
              fontSize: "20px"
            },
            formatter: function(val) {
              return `${format(",.0f")(val)}`;
            }
          },
          title: {
            text: "Number of Employees in FY20",
            offsetX: -10,
            style: {
              fontSize: "20px"
            }
          },
          forceNiceScale: true
        },

        colors: this.data["colors"]
      };
    },
    series() {
      return this.data["data"];
    }
  }
};
</script>



