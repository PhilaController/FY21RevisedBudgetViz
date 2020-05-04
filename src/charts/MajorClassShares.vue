<template>
  <div>
    <div v-for="(col, i) in major_classes" :key="col">
      <div class="text-center font-italic">{{ col }}</div>
      <MajorClassShareChart
        :data="data[col]"
        :categories="data['fiscal_year']"
        :height="height"
        :color="colors[i]"
        :width="width"
      />
    </div>
  </div>
</template>

<script>
import MajorClassShareChart from "@/charts/MajorClassShareChart.vue";

export default {
  components: { MajorClassShareChart },
  props: ["width", "height"],
  data() {
    return {
      data: require("@/data/by_major_class_normalized.json"),
      colors: [
        "#2176d2",
        "#58c04d",
        "#f3c613",
        "#f99300",
        "#f40000",
        "#d233ff",
        "#25cef7"
      ]
    };
  },
  computed: {
    major_classes() {
      let out = [];
      for (let col in this.data) {
        if (col != "fiscal_year") out.push(col);
      }
      return out;
    }
  }
};
</script>
