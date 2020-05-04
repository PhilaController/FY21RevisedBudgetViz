<template>
  <VueApexCharts
    :width="width"
    :height="height"
    :data="data"
    type="line"
    :options="chartOptions"
    :series="series"
  ></VueApexCharts>
</template>

<script>
import VueApexCharts from "vue-apexcharts";
import { format } from "d3-format";

export default {
  components: { VueApexCharts },
  props: ["width", "height", "data", "categories", "color"],
  computed: {
    chartOptions() {
      return {
        grid: {
          padding: {
            left: 30,
            right: 30,
            top: 30,
            bottom: 30
          }
        },
        annotations: {
          points: [
            {
              x: 1,
              y: this.data[0],
              marker: {
                size: 8,
                fillColor: "#fff",
                strokeColor: this.color,
                strokeWidth: 4
              },
              label: {
                borderColor: "none",
                offsetY: -5,
                style: {
                  fontSize: "1.1rem",
                  color: "#444444",
                  background: "none"
                },

                text: `${format(".1f")(100 * this.data[0])}%`
              }
            },
            {
              x: this.data.length,
              y: this.data[this.data.length - 1],
              marker: {
                size: 8,
                fillColor: "#fff",
                strokeColor: this.color,
                strokeWidth: 4
              },
              label: {
                borderColor: "none",
                offsetY: -5,
                textAnchor: "start",
                style: {
                  fontSize: "1.1rem",
                  color: "#444444",
                  background: "none"
                },

                text: `${format(".1f")(100 * this.data[this.data.length - 1])}%`
              }
            }
          ]
        },
        dataLabels: {
          enabled: false
        },
        chart: {
          sparkline: {
            enabled: true
          }
        },
        markers: {
          size: 0,
          strokeColor: this.color,
          colors: ["#ffffff"],
          strokeWidth: 4
        },
        tooltip: {
          enabled: true,
          style: { fontSize: "20px" },
          y: {
            formatter: function(val) {
              return `${format(".1f")(100 * val)}%`;
            }
          }
        },
        xaxis: {
          show: false,
          type: "categories",
          categories: this.categories,
          labels: {
            show: false
          },
          crosshairs: { show: false },
          min: 0,
          max: this.categories.length + 1,
          tooltip: { enabled: false }
        },
        yaxis: {
          show: false
        },

        colors: [this.color]
      };
    },
    series() {
      return [{ name: "", data: this.data }];
    }
  }
};
</script>

