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
      data: require("@/data/historical_payroll.json")
    };
  },
  computed: {
    chartOptions() {
      return {
        annotations: {
          position: "back",
          yaxis: [
            {
              y: this.data["class_100"][this.data["class_100"].length - 3],
              y2: this.data["class_100"][this.data["class_100"].length - 1],
              borderColor: "#666",
              fillColor: "#666",
              borderWidth: 0,
              opacity: 0.2,
              label: {
                borderColor: "none",
                style: {
                  fontSize: "25px",
                  color: "#444444",
                  background: "none",
                  borderWidth: 0
                },
                text: "+8%",
                textAnchor: "start",
                offsetY: 60,
                offsetX: -80
              }
            }
          ]
        },
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
              return `$${format(".2f")(val)}B`;
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
          decimalsInFloat: 1,
          labels: {
            style: {
              fontSize: "20px"
            },
            formatter: function(val) {
              return `$${format(".1f")(val)}B`;
            }
          },
          min: 1.2,
          forceNiceScale: true,
          crosshairs: { show: false }
        },

        colors: ["#cc3000"]
      };
    },
    series() {
      return [{ name: "", data: this.data["class_100"] }];
    }
  }
};
</script>



