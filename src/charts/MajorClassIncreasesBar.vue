<template>
  <VueApexCharts :width="width" :height="height" :options="chartOptions" :series="series"></VueApexCharts>
</template>

<script>
import VueApexCharts from "vue-apexcharts";
import { format } from "d3-format";

export default {
  props: ["height", "width"],
  components: {
    VueApexCharts
  },
  data() {
    return {
      data: require("@/data/increases_by_major_class.json")
    };
  },

  computed: {
    chartOptions() {
      return {
        chart: {
          type: "bar",
          toolbar: {
            show: false
          }
        },
        plotOptions: {
          bar: {
            horizontal: true,
            distributed: true
          }
        },
        dataLabels: {
          enabled: false
        },
        xaxis: {
          categories: this.data["major_class_description"],
          labels: {
            style: {
              fontSize: "15px"
            },
            formatter: function(val) {
              return `$${format(".0f")(val)}M`;
            }
          }
        },
        yaxis: { labels: { minWidth: 250, maxWidth: 300 } },
        colors: [
          "#2176d2",
          "#d233ff",
          "#f99300",
          "#58c04d",
          "#f3c613",
          "#f40000"
        ],
        tooltip: {
          y: {
            formatter: function(value) {
              return "$" + format(",.1f")(value) + "M";
            }
          },
          style: { fontSize: "1rem" }
        },
        legend: {
          show: false
        }
      };
    },
    series() {
      return [{ name: "", data: this.data["diff"] }];
    }
  }
};
</script>