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
      data: require("@/data/historical_employees.json")
    };
  },
  computed: {
    chartOptions() {
      return {
        annotations: {
          points: [
            {
              x: 13.5,
              y: 21100,
              marker: {
                size: 0,
                radius: 0
              },
              label: {
                borderColor: "none",
                offsetY: 0,
                style: {
                  background: "none",
                  fontSize: "30px"
                },

                text: "+945"
              }
            },
            {
              x: 4.15,
              y: 20100,
              marker: {
                size: 0,
                radius: 0
              },
              label: {
                borderColor: "none",
                offsetY: 0,
                style: {
                  background: "none",
                  fontSize: "30px"
                },

                text: "\u2212" + "975"
              }
            }
          ]
        },
        dataLabels: {
          enabled: false
        },
        chart: {
          zoom: { enabled: false },
          toolbar: {
            show: false
          }
        },
        grid: {
          padding: { left: 25, right: 25, bottom: -20 }
        },
        markers: {
          size: 7,
          strokeColor: "#666666",
          colors: ["#ffffff"],
          strokeWidth: 4
        },
        tooltip: {
          enabled: true,
          enabledOnSeries: [0],
          style: { fontSize: "20px" },
          y: {
            formatter: function(val) {
              return `${format(",.0f")(val)}`;
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
          forceNiceScale: true,
          crosshairs: { show: false }
        },

        colors: ["#666666", "#b9f2b1", "#fed0d0"]
      };
    },
    series() {
      let series2 = [],
        series3 = [];
      let FY;
      for (let i = 0; i < this.data["fiscal_year"].length; i++) {
        FY = this.data["fiscal_year"][i];
        if ((FY >= 2008) & (FY <= 2011)) {
          series3.push(this.data["total_employees"][i]);
        } else {
          series3.push(null);
        }
        if ((FY >= 2017) & (FY <= 2020)) {
          series2.push(this.data["total_employees"][i]);
        } else {
          series2.push(null);
        }
      }
      return [
        { name: "", type: "line", data: this.data["total_employees"] },
        {
          name: "2",
          type: "area",
          data: series2
        },
        {
          name: "3",
          type: "area",
          data: series3
        }
      ];
    }
  }
};
</script>



