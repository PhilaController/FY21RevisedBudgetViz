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
      data: require("@/data/by_major_class.json")
    };
  },
  computed: {
    chartOptions() {
      return {
        yaxis: {
          labels: {
            formatter: function(val) {
              return `$${format(",.0f")(val / 1e3)}B`;
            }
          }
        },
        chart: {
          type: "bar",
          stacked: true,
          toolbar: { show: false }
        },
        legend: {
          show: true,
          position: "top",
          fontSize: "15px",
          fontFamily: '"Avenir", Helvetica, Arial, sans-serif',
          markers: { width: 16, height: 16, radius: 16 },
          offsetY: 0
        },
        colors: [
          "#2176d2",
          "#58c04d",
          "#f3c613",
          "#f99300",
          "#f40000",
          "#d233ff",
          "#25cef7"
        ],
        dataLabels: {
          enabled: false
        },
        plotOptions: {
          bar: {
            horizontal: false,
            columnWidth: "60%"
          }
        },
        xaxis: {
          categories: this.data["fiscal_year"],
          labels: { rotate: -90, rotateAlways: true }
        },
        tooltip: {
          y: {
            formatter: function(value) {
              return "$" + format(",.1f")(value) + "M";
            }
          },
          style: { fontSize: "1rem" }
        }
        // responsive: [
        //   {
        //     breakpoint: 1000,
        //     options: {
        //       yaxis: {
        //         labels: {
        //           show: false
        //         }
        //       },
        //       xaxis: { tickAmount: 3, labels: { trim: false } },
        //       dataLabels: {
        //         enabled: true,
        //         textAnchor: "start",
        //         style: {
        //           colors: ["#121516"]
        //         },
        //         formatter: (val, opt) => {
        //           if (
        //             opt.seriesIndex == 0 ||
        //             val === this.totals[opt.dataPointIndex]
        //           )
        //             return opt.w.globals.labels[opt.dataPointIndex];
        //         }
        //       }
        //     }
        //   }
        // ]
      };
    },
    series() {
      let out = [];
      for (let col in this.data) {
        if (col != "fiscal_year") out.push({ name: col, data: this.data[col] });
      }
      return out;
    }
  }
};
</script>

<style>
.apexcharts-yaxis-label,
.apexcharts-xaxis-label {
  font-size: 1.1rem;
  font-family: "Avenir", Helvetica, Arial, sans-serif;
}
</style>