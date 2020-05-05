<template>
  <svg :width="width" :height="height">
    <g id="color-key-canvas" />
  </svg>
</template>

<script>
import * as d3 from "d3";

export default {
  props: ["colorScale", "width", "height"],
  data() {
    return {
      margin: { right: 30, bottom: 30, left: 30 },
      barHeight: 20
    };
  },
  computed: {
    axisScale() {
      return d3
        .scaleLinear()
        .domain(this.colorScale.domain())
        .range([this.margin.left, this.width - this.margin.right]);
    }
  },
  watch: {
    colorScale(newValue, oldValue) {
      if (newValue) {
        let svg = d3.select("#color-key-canvas");
        const defs = svg.append("defs");

        const linearGradient = defs
          .append("linearGradient")
          .attr("id", "linear-gradient");

        linearGradient
          .selectAll("stop")
          .data(
            this.colorScale.ticks().map((t, i, n) => ({
              offset: `${(100 * i) / n.length}%`,
              color: this.colorScale(t)
            }))
          )
          .enter()
          .append("stop")
          .attr("offset", d => d.offset)
          .attr("stop-color", d => d.color);

        svg
          .append("g")
          .attr(
            "transform",
            `translate(0,${this.height - this.margin.bottom - this.barHeight})`
          )
          .append("rect")
          .attr("transform", `translate(${this.margin.left}, 0)`)
          .attr("width", this.width - this.margin.right - this.margin.left)
          .attr("height", this.barHeight)
          .style("fill", "url(#linear-gradient)");

        svg.append("g").call(this.axisBottom);
      }
    }
  },
  methods: {
    axisBottom(g) {
      return g
        .attr("class", `x-axis`)
        .attr("transform", `translate(0,${this.height - this.margin.bottom})`)
        .call(
          d3
            .axisBottom(this.axisScale)
            .ticks(this.width / 80)
            .tickSize(-this.barHeight)
            .tickFormat(d3.format("+.0%"))
        );
    }
  }
};
</script>

<style>
.x-axis line,
.x-axis path {
  stroke: #fff;
}

.tick text {
  font-size: 1rem;
  fill: #2c3e50;
}
</style>
