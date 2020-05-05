<template>
  <div class="legend-wrapper d-flex justify-content-center">
    <!-- Color key -->
    <div class="color-key-wrapper d-flex flex-column">
      <div class="legend-title d-flex justify-content-center mb-2">
        <div>
          <span class="font-weight-bold">Bubble color</span> shows the
          <span class="font-weight-bold">percentage change</span>
          in {{ label }}.
        </div>
      </div>
      <ColorKey :colorScale="colorScale" :width="width" height="50" />
    </div>
    <!-- Radius key -->
    <div class="radius-key-wrapper d-flex flex-column">
      <div class="legend-title d-flex flex-row justify-content-center">
        <div>
          <span class="font-weight-bold">Bubble size</span> shows the
          <span class="font-weight-bold">dollar change</span>
          in {{ label }}.
        </div>
      </div>
      <RadiusKey :radiusScale="radiusScale" :width="width" :sizes="sizes" :height="radiusHeight" />
    </div>
  </div>
</template>

<script>
import ColorKey from "./ColorKey";
import RadiusKey from "./RadiusKey";
import * as d3 from "d3";

export default {
  props: ["colorScale", "radiusScale", "sizes", "label"],
  components: { ColorKey, RadiusKey },
  data() {
    return {};
  },
  computed: {
    width() {
      return Math.min(window.screen.width * 0.9, 500);
    },
    radiusHeight() {
      return window.screen.width > 768 ? 110 : 75;
    }
  }
};
</script>

<style>
.color-key-wrapper,
.radius-key-wrapper {
  max-width: 500px !important;
}
.color-key-wrapper {
  margin-right: 10px;
}
.radius-key-wrapper {
  margin-left: 10px;
}
.legend-wrapper {
  font-size: 1.1rem;
}

@media screen and (max-width: 1024px) {
  .legend-wrapper {
    flex-direction: column;
    align-items: center;
  }
  .radius-key-wrapper {
    margin-top: 20px;
  }
  .color-key-wrapper {
    margin-right: 0px;
  }
  .radius-key-wrapper {
    margin-left: 0px;
  }
}
</style>
