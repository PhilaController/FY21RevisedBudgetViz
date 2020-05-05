<template>
  <svg :width="width" :height="height">
    <g id="radius-key-canvas" />
  </svg>
</template>

<script>
import * as d3 from "d3";

export default {
  props: ["radiusScale", "width", "sizes", "height"],
  data() {
    return {
      margin: { right: 40, bottom: 0, left: 40, top: 0 }
    };
  },
  watch: {
    radiusScale(newValue, oldValue) {
      if (newValue) {
        let svg = d3
          .select("#radius-key-canvas")
          .attr(
            "transform",
            `translate(${this.width / 2}, ${this.height / 2})`
          );

        // add circles
        let circles = svg
          .selectAll("circle")
          .data(this.sizes)
          .enter()
          .append("circle")
          .attr("r", d => newValue(d))
          .attr("cy", d => this.height / 2 - this.margin.bottom - newValue(d))
          .attr("cx", 0)
          .attr("fill", "none")
          .attr("stroke", "#cfcfcf")
          .attr("stroke-dasharray", "5,5")
          .attr("stroke-width", 2);

        // add text
        let texts = svg
          .selectAll("text")
          .data(this.sizes)
          .enter()
          .append("text")
          .text(d => `$${d3.format(",.1s")(d)}`)
          .attr("fill", "#2c3e50")
          .attr("font-size", "1.1rem")
          .attr("font-family", "sans-serif")
          .attr("dx", "4.5em")
          .attr(
            "y",
            d => this.height / 2 - this.margin.bottom - 2 * newValue(d)
          )
          .attr("alignment-baseline", d => (d == 1 ? "hanging" : "baseline"));

        // add lines
        let lines = svg
          .selectAll("line")
          .data(this.sizes)
          .enter()
          .append("line")
          .attr("x1", 0)
          .attr("x2", "4em")
          .attr("stroke-width", 1.25)
          .attr("stroke", "#2c3e50")
          .attr(
            "y1",
            d => this.height / 2 - this.margin.bottom - 2 * newValue(d)
          )
          .attr(
            "y2",
            d => this.height / 2 - this.margin.bottom - 2 * newValue(d)
          );
      }
    }
  }
};
</script>

<style>
.radius-label {
  font: italic 13px sans-serif;
}
</style>
