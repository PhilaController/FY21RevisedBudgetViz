<template>
  <div class="d-flex justify-content-center" id="color-key">
    <!-- Color key -->
    <div class="color-key-wrapper d-flex flex-column justify-content-start">
      <div class="legend-title d-flex justify-content-center">
        <div>
          <span class="font-weight-bold">Bubble color</span> shows the
          <span class="font-weight-bold">percentage change</span> in projected revenue.
        </div>
      </div>
      <ColorKey :colorScale="colorScale" :width="400" />
    </div>
    <!-- Radius key -->
    <div class="radius-key-wrapper ml-5 d-flex flex-column justify-content-center">
      <div class="legend-title d-flex flex-row justify-content-center">
        <div>
          <span class="font-weight-bold">Bubble size</span> shows the
          <span class="font-weight-bold">dollar change</span> in projected revenue.
        </div>
      </div>
      <RadiusKey :radiusScale="radiusScale" :width="500" :sizes="[1e6, 50e6, 200e6]" />
    </div>
  </div>
</template>

<script>
import ColorKey from "./ColorKey";
import RadiusKey from "./RadiusKey";
import * as d3 from "d3";

export default {
  props: ["colorScale", "radiusScale"],
  components: { ColorKey, RadiusKey },
  data() {
    return {};
  }
};
</script>

<style>
.color-key-wrapper,
.radius-key-wrapper {
  max-width: 500px !important;
}
</style>
