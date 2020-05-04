<template>
  <div>
    <!-- Bubbles -->
    <div>
      <Legend :colorScale="fillColorScale" :radiusScale="radiusScale" />
      <div class="budget-explorer-viz"></div>
    </div>

    <!-- Table -->
    <div class="mt-5">
      <VueGoodTable
        ref="budgetRevenueTable"
        :columns="tableColumns"
        :rows="tableRows"
        styleClass="vgt-table condensed"
        @on-sort-change="onSortChange"
        :sort-options="{
          enabled: true,
          initialSortBy: {field: this.sortColumn, type: this.sortOrder}
        }"
        :group-options="groupOptions"
      ></VueGoodTable>
    </div>
  </div>
</template>

<script>
import Legend from "./Legend";
import { formatFn, netChangeFormatFn } from "@/utils/formatFns";
import * as d3 from "d3";
import d3Tip from "d3-tip";
import { rollup, group } from "d3-array";
import "vue-good-table/dist/vue-good-table.css";
import { VueGoodTable } from "vue-good-table";

export default {
  props: ["width", "fiscalYear", "viewingMode", "rawData"],
  components: { Legend, VueGoodTable },
  data() {
    return {
      margin: { top: 30, right: 10, bottom: 10, left: 10 },

      // How to arrange the different viewing modes
      gridConfig: {
        "All Changes": { columns: 1, height: 250 },
        "By Revenue Source": {
          columns: 3,
          height: 300,
          groupby: "revenue_source"
        }
      },
      // Components of the viz
      radiusScale: null,
      fillColorScale: null,
      yOffsetScale: null,
      svg: null,
      innerSVG: null,
      bubbles: null,
      nodes: null,
      gridLayout: null,
      forceSim: null,
      tooltip: null,
      splitView: false, // is the viewing mode one big circle or split
      addAnnotations: false, // arrows/labels showing cuts/increases?,
      sortColumn: "percent_diff",
      sortOrder: "asc"
    };
  },
  mounted() {
    this.$nextTick(() => {
      // Initialize tooltip
      this.tooltip = d3Tip().attr("class", "tooltip");

      // Setup the radius scale
      this.radiusScale = this.getRadiusScale(this.rawData, 40);

      // Sort bubbles by percent change
      this.yOffsetScale = d3
        .scaleQuantile()
        .domain([-1, 1])
        .range([10, 5, -5, -10]);

      // Color bubbles by the percent change
      this.fillColorScale = d3
        .scaleSequential()
        .interpolator(
          d3.interpolateRgbBasis([
            "#da3b46",
            "#e05b65",
            "#e67c84",
            "#ed9da3",
            "#f3c0c4",
            "#f9e1e3",
            "#e5f2e7",
            "#c3ddc8",
            "#9fc6a7",
            "#7db188",
            "#5b9b69",
            "#398649"
          ])
        )
        .domain([-0.3, 0.3])
        .clamp(true);

      this.colorPercentDiffCells();

      // Initialize the "nodes" with the data we've loaded
      this.nodes = this.createNodes(this.rawData);

      // Initialize svg and innerSVG, which we will attach all our drawing objects to.
      this.createCanvas(".budget-explorer-viz");

      /* Invoke the tip in the context of your visualization */
      this.svg.call(this.tooltip);

      // Create the bubbles and the force holding them apart
      this.createBubbles();

      // Set the viewing mode
      this.setViewingMode(false);
    });
  },
  computed: {
    groupOptions() {
      let t = this.viewingMode !== "All Changes";
      return {
        enabled: t,
        collapsable: t
      };
    },
    tableColumns() {
      let percentFn = d => {
        let s = `${(100 * Math.abs(d)).toFixed(0)}%`;
        if (d < 0) s = "\u2212" + s;
        return s;
      };

      let cols;
      if (this.viewingMode !== "By Revenue Source")
        cols = [
          {
            label: "Name",
            field: "name"
          },
          {
            label: "Revenue Source",
            field: "revenue_source"
          }
        ];
      else
        cols = [
          {
            label: "Revenue Source",
            field: "revenue_source"
          },
          {
            label: "Name",
            field: "name"
          }
        ];

      cols.push(
        {
          label: "Proposed",
          field: `${this.fiscalYear} (Proposed)`,
          type: "number",
          formatFn: formatFn
        },
        {
          label: "Revised",
          field: `${this.fiscalYear} (Revised)`,
          type: "number",
          formatFn: formatFn
        },
        {
          label: "Net Change",
          field: "diff",
          type: "number",
          formatFn: netChangeFormatFn
        },
        {
          label: "Percent Change",
          field: "percent_diff",
          type: "number",
          formatFn: percentFn
        }
      );
      return cols;
    },
    tableRows() {
      let out = [],
        row,
        child,
        col,
        grouped;

      if (this.viewingMode == "By Revenue Source")
        grouped = group(this.rawData, d => d.revenue_source);
      else grouped = group(this.rawData, d => d.name);

      let id = 0;
      for (let [k, v] of grouped) {
        row = { id: id, children: [] };
        if (this.viewingMode == "By Revenue Source") row["revenue_source"] = k;
        else row["name"] = k;

        // Total Proposed
        row[`${this.fiscalYear} (Proposed)`] = d3.sum(
          v,
          d => d[`${this.fiscalYear} (Proposed)`]
        );

        // Total Revised
        row[`${this.fiscalYear} (Revised)`] = d3.sum(
          v,
          d => d[`${this.fiscalYear} (Revised)`]
        );

        // Diff
        row["diff"] =
          row[`${this.fiscalYear} (Revised)`] -
          row[`${this.fiscalYear} (Proposed)`];

        // if (row["diff"] == 0) continue;

        // Percent diff
        row["percent_diff"] =
          row["diff"] / row[`${this.fiscalYear} (Proposed)`];

        out.push(row);

        for (let i = 0; i < v.length; i++) {
          child = {};

          // Name and major class
          child["name"] = v[i].name;
          child["revenue_source"] = v[i].revenue_source;

          // Revised
          child[`${this.fiscalYear} (Revised)`] =
            v[i][`${this.fiscalYear} (Revised)`];

          // Proposed
          child[`${this.fiscalYear} (Proposed)`] =
            v[i][`${this.fiscalYear} (Proposed)`];

          // Differnce
          child["diff"] =
            v[i][`${this.fiscalYear} (Revised)`] -
            v[i][`${this.fiscalYear} (Proposed)`];

          // Percent diff
          child["percent_diff"] =
            child["diff"] / v[i][`${this.fiscalYear} (Proposed)`];

          // Add if there's a difference
          // if (child["diff"] != 0)
          row["children"].push(child);
        }
        id += 1;
      }

      let sortFn = this.sortOrder == "asc" ? d3.ascending : d3.descending;
      return out.sort((x, y) => sortFn(x[this.sortColumn], y[this.sortColumn]));
    },
    height() {
      return this.gridConfig[this.viewingMode].height;
    },
    tooltipConfig() {
      return [
        {
          title: "Revenue Source",
          data_field: "revenue_source"
        },
        {
          title: `${this.fiscalYear} (Original)`,
          data_field: `${this.fiscalYear} (Proposed)`,
          format_string: ",.3s"
        },
        {
          title: `${this.fiscalYear} (Revised)`,
          data_field: `${this.fiscalYear} (Revised)`,
          format_string: ",.3s"
        },
        {
          title: "Net Change",
          data_field: "actual_radius",
          format_string: ",.3s"
        },
        {
          title: "Percent Change",
          data_field: "percent_diff",
          format_string: "+.1%"
        }
      ];
    },
    canvasWidth() {
      return this.width - this.margin.left - this.margin.right;
    },
    canvasHeight() {
      return this.height - this.margin.top - this.margin.bottom;
    },
    force_type() {
      return "charge";
    },
    force_strength() {
      return 0.1;
    }
  },
  watch: {
    height(newValue, oldValue) {
      if (this.svg) this.svg.attr("height", newValue);
    },
    fiscalYear(newValue, oldValue) {
      this.handleYearChange();
    },
    tableRows(newValue, oldValue) {
      this.$nextTick(() => {
        this.colorPercentDiffCells();
      });
    },
    viewingMode(newMode, oldMode) {
      // Set the split view boolean
      this.splitView = newMode != "All Changes";

      // Handle updates to viewing mode
      this.$nextTick(() => {
        // handle the annotations
        if (!this.splitView) this.addAnnotations = false;
        else this.svg.selectAll(".budget_annotation").remove();

        // set the viewing mode
        this.setViewingMode(true);

        // Handle the group labels
        if (!this.splitView)
          this.innerSVG.selectAll(".bubble_group_label").remove();
      });
    }
  },
  methods: {
    colorPercentDiffCells() {
      if (this.fillColorScale) {
        let rows = $(this.$refs.budgetRevenueTable.$el).find("tr");

        let cellType = this.viewingMode !== "All Changes" ? "th" : "td";

        rows.find(`${cellType}:nth-child(6)`).each((i, x) => {
          let p = $(x)[0].innerText.slice(0, -1);
          if (p.startsWith("\u2212")) p = (-1 * parseFloat(p.slice(1))) / 100;
          else p = parseFloat(p) / 100;

          $(x).css("background-color", this.fillColorScale(p));
          $(x).css("border-bottom-color", this.fillColorScale(p));
        });
      }
    },
    onSortChange(params) {
      this.sortColumn = params[0].field;
      this.sortOrder = params[0].type;

      this.colorPercentDiffCells();
    },
    handleYearChange() {
      /* 
        Function to update visualization when a new fiscal year is chosen
      */
      // Only need to do something if nodes exist
      if (this.nodes) {
        // Update the radii based on the new selected years
        this.nodes = this.updateNodes(this.nodes);

        // remove annotations for now
        this.addAnnotations = false;

        // Circles with new data
        let circles = this.innerSVG.selectAll(".bubble").data(
          this.nodes, //.filter(d => d.actual_radius !== 0),
          d => d.id
        );

        // Update selection --> transition to new radius
        circles
          .transition()
          .duration(1000)
          .attr("r", function(d) {
            return d.scaled_radius;
          })
          .attr("fill", d => {
            return this.fillColorScale(this.getSpendingDiffPercent(d));
          })
          .attr("stroke", d => {
            return d3
              .rgb(this.fillColorScale(this.getSpendingDiffPercent(d)))
              .darker();
          });

        // Enter selection
        circles
          .enter()
          .append("circle")
          .attr("r", d => d.scaled_radius)
          .classed("bubble", true)
          .attr("fill", d => {
            return this.fillColorScale(this.getSpendingDiffPercent(d));
          })
          .attr("stroke", d => {
            return d3
              .rgb(this.fillColorScale(this.getSpendingDiffPercent(d)))
              .darker();
          })
          .attr("stroke-width", 1)
          .on("mouseover", this.showTooltip)
          .on("mouseout", this.hideTooltip);

        // Remove
        circles.exit().remove();

        // Update bubbles
        this.bubbles = d3.selectAll(".bubble");

        // Update the viewing modes
        this.setViewingMode(false);

        // (re)initialize the forces
        this.forceSim.force(this.force_type).initialize(this.nodes);
      }
    },

    getRadiusScale(data, maxPixels) {
      /* 
        Generate a scale to go from radius to pixels
      */

      // Maximum possible dollar difference
      let diffMax = d3.max(data, d =>
        Math.abs(
          d[`${this.fiscalYear} (Revised)`] - d[`${this.fiscalYear} (Proposed)`]
        )
      );
      return d3
        .scalePow()
        .exponent(0.5)
        .range([7, maxPixels])
        .domain([0, diffMax]);
    },

    getSpendingDiff(d, absFlag) {
      /* 
        Utility function to calculate spending difference
      */
      // Do revised minus proposed
      let diff =
        d[`${this.fiscalYear} (Revised)`] - d[`${this.fiscalYear} (Proposed)`];
      if (absFlag) diff = Math.abs(diff);
      return diff;
    },

    getSpendingDiffPercent(d, absFlag) {
      /* 
        Utility function to calculate percent spending change
      */

      let diff = this.getSpendingDiff(d, false);
      let toret = diff / d[`${this.fiscalYear} (Proposed)`];
      if (diff == 0 && d[`${this.fiscalYear} (Revised)`] == 0) toret = 0;
      return toret;
    },

    createNodes(data) {
      /* 
        Create the nodes for the force simulation from the input raw data
      */

      // Use map() to convert raw data into node data.
      let node, diff;
      let myNodes = data.map((data_row, i) => {
        diff = this.getSpendingDiff(data_row, true);
        node = {
          id: i,
          scaled_radius: this.radiusScale(diff),
          actual_radius: diff,
          x: Math.random() * this.canvasWidth,
          y: Math.random() * this.canvasHeight,
          percent_diff: this.getSpendingDiffPercent(data_row)
        };
        for (let key in data_row) {
          // Skip loop if the property is from prototype
          if (!data_row.hasOwnProperty(key)) continue;
          node[key] = data_row[key];
        }

        return node;
      });

      // Sort them to prevent occlusion of smaller nodes.
      myNodes.sort(function(a, b) {
        return b.actual_radius - a.actual_radius;
      });

      return myNodes;
    },

    updateNodes(nodes) {
      /*
        Update the scaled radius in the nodes,
        which will use currently selected fiscal year
      */
      let diff;
      let myNodes = nodes.map(node => {
        diff = this.getSpendingDiff(node, true);
        node = Object.assign(node, {
          scaled_radius: this.radiusScale(diff),
          actual_radius: diff,
          percent_diff: this.getSpendingDiffPercent(node)
        });

        return node;
      });

      // Sort them to prevent occlusion of smaller nodes.
      myNodes.sort(function(a, b) {
        return b.actual_radius - a.actual_radius;
      });

      return myNodes;
    },
    createCanvas() {
      // Create a SVG element inside the provided selector with desired size.
      this.svg = d3
        .select(".budget-explorer-viz")
        .append("svg")
        .attr("width", this.width)
        .attr("height", this.height);

      // Create an inner SVG panel with padding on all sides for axes
      this.innerSVG = this.svg
        .append("g")
        .attr(
          "transform",
          `translate(${this.margin.left}, ${this.margin.top})`
        );
    },
    createBubbles() {
      // Bind nodes data to what will become DOM elements to represent them.
      this.innerSVG
        .selectAll(".bubble")
        .data(
          this.nodes, //.filter(d => d.actual_radius !== 0),
          d => d.id
        )
        .enter()
        .append("circle")
        .attr("r", 0) // Initially, their radius (r attribute) will be 0.
        .classed("bubble", true)
        .attr("fill", d => {
          return this.fillColorScale(this.getSpendingDiffPercent(d));
        })
        .attr("stroke", d => {
          return d3
            .rgb(this.fillColorScale(this.getSpendingDiffPercent(d)))
            .darker();
        })
        .attr("stroke-width", 1)
        .on("mouseover", this.showTooltip)
        .on("mouseout", this.hideTooltip);

      this.bubbles = d3.selectAll(".bubble");

      // Fancy transition to make bubbles appear, ending with the correct radius
      this.bubbles
        .transition()
        .duration(1000)
        .attr("r", function(d) {
          return d.scaled_radius;
        });
    },
    getGridLayout(groupby, singleBubble) {
      /* 
        Get the grid layout for the current viewing mode
      */
      let out, labels;

      // one big bubble
      if (singleBubble) {
        out = {
          labels: [""],
          gridDimensions: { rows: 1, columns: 1 },
          dataField: null,
          size: 1
        };
      } else {
        // This is the key the grid will be grouped by
        groupby = this.gridConfig[groupby].groupby;

        // Determine the labels to show
        labels = Array.from(
          rollup(
            this.rawData,
            v =>
              d3.sum(
                v,
                d =>
                  d[`${this.fiscalYear} (Revised)`] -
                  d[`${this.fiscalYear} (Proposed)`]
              ),
            d => d[groupby]
          )
        )
          .sort((x, y) => d3.ascending(x[1], y[1]))
          // .filter(item => item[1] !== 0)
          .map(item => item[0])
          .filter((value, index, self) => self.indexOf(value) === index);

        let numCols = this.gridConfig[this.viewingMode].columns;
        out = {
          labels: labels,
          gridDimensions: {
            rows: Math.floor(labels.length / numCols),
            columns: numCols
          },
          dataField: groupby,
          size: labels.length
        };
        if (labels.length % numCols > 0) out.gridDimensions.rows += 1;
      }

      // Loop through all grid labels and assign the centre coordinates
      out.gridCenters = {};
      for (let i = 0; i < out.size; i++) {
        let cur_row = Math.floor(i / out.gridDimensions.columns); // indexed starting at zero
        let cur_col = i % out.gridDimensions.columns; // indexed starting at zero
        let currentCenter = {
          x:
            (2 * cur_col + 1) *
            (this.canvasWidth / (out.gridDimensions.columns * 2)),
          y:
            (2 * cur_row + 1) *
            (this.canvasHeight / (out.gridDimensions.rows * 2))
        };
        out.gridCenters[out.labels[i]] = currentCenter;
      }

      return out;
    },
    getGridTargetFunction(layout) {
      /*
        Determine the mapping between node and target location
      */
      return node => {
        let target, node_tag;
        // Given a mode and node, return the correct target
        if (layout.size == 1) {
          // If there is no grid, our target is the default center
          target = Object.assign({}, layout.gridCenters[""]);
          if (!this.splitView)
            target.y =
              target.y + Math.round(this.yOffsetScale(node.percent_diff));
        } else {
          // If the grid size is greater than 1, look up the appropriate target
          // coordinate using the relevant node_tag for the mode we are in
          node_tag = node[layout.dataField];

          if (layout.gridCenters[node_tag]) {
            target = {
              x: layout.gridCenters[node_tag].x,
              y: layout.gridCenters[node_tag].y
            };
          } else {
            target = {
              x: -1000,
              y: -1000
            };
          }

          if (this.viewingMode == "By Revenue Source") {
            target.y =
              target.y + Math.round(this.yOffsetScale(node.percent_diff));
          }
        }
        return target;
      };
    },
    ticked() {
      /* 
        The function that runs at each tick of the simulation
      */
      this.bubbles
        .each(node => {})
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);

      if (
        !this.splitView &&
        !this.addAnnotations &&
        this.forceSim.alpha() < 0.9
      ) {
        this.addAnnotations = true;
        let xcoords = [],
          ycoords = [];
        this.bubbles.each(node => {
          xcoords.push(node.x);
          ycoords.push(node.y);
        });
        let xextent = d3.extent(xcoords);
        let yextent = d3.extent(ycoords);
        let xcenter = 0.5 * (xextent[0] + xextent[1]);

        // Add annotioan labels
        let labels = ["Revenue increases", "Revenue decreases"];
        let t = d3.transition().duration(1000);
        let texts = this.svg.selectAll("text").data(yextent);
        texts
          .enter()
          .append("text")
          .text((d, i) => labels[i])
          .attr("fill", "#2c3e50")
          .attr("class", "budget_annotation")
          .attr("font-size", "1.1rem")
          .attr("font-family", "sans-serif")
          .merge(texts)
          .transition(t)
          .attr("x", xextent[1])
          .attr("y", (d, i) => {
            let offset = i == 0 ? 10 : -10;
            return yextent[i] + this.margin.top + offset;
          })
          .attr("alignment-baseline", "middle");

        // add lines
        let lines = this.svg.selectAll("line").data(yextent);
        lines
          .enter()
          .append("line")
          .attr("stroke-width", 1.25)
          .attr("stroke", "#2c3e50")
          .attr("stroke-dasharray", "5,5")
          .attr("class", "budget_annotation")
          .merge(lines)
          .transition(t)
          .attr("x1", xcenter)
          .attr("x2", xextent[1] - 10)
          .attr("y1", (d, i) => {
            let offset = i == 0 ? 10 : -10;
            return yextent[i] + this.margin.top + offset;
          })
          .attr("y2", (d, i) => {
            let offset = i == 0 ? 10 : -10;
            return yextent[i] + this.margin.top + offset;
          });
      }
    },

    setViewingMode(addForceTransition) {
      // Get the grid layout
      this.gridLayout = this.getGridLayout(this.viewingMode, !this.splitView);

      // Show labels if we need to
      if (this.gridLayout.size > 1) {
        this.showLabels(this.gridLayout);
      }

      // Add the force layout
      this.addForceLayout();

      // Move the bubbless
      let targetFunction = this.getGridTargetFunction(this.gridLayout);

      // Given the mode we are in, obtain the node -> target mapping
      let targetForceX = d3
        .forceX(function(d) {
          return targetFunction(d).x;
        })
        .strength(+this.force_strength);
      let targetForceY = d3
        .forceY(function(d) {
          return targetFunction(d).y;
        })
        .strength(+this.force_strength);

      // Specify the target of the force layout for each of the circles
      this.forceSim.force("x", targetForceX).force("y", targetForceY);

      // Restart the force layout simulation
      this.forceSim
        .alpha(1)
        .alphaMin(0.001)
        .alphaDecay(0.001)
        .alphaTarget(0)
        .restart();
    },
    addForceLayout() {
      if (this.forceSim) {
        // Stop any forces currently in progress
        this.forceSim.stop();
      }
      // Configure the force layout holding the bubbles apart
      this.forceSim = d3
        .forceSimulation()
        .nodes(this.nodes)
        .velocityDecay(0.3)
        .on("tick", this.ticked);

      // Decide what kind of force layout to use: "collide" or "charge"
      if (this.force_type == "collide") {
        let bubbleCollideForce = d3
          .forceCollide()
          .radius(function(d) {
            return d.scaled_radius + 0.5;
          })
          .iterations(4);
        this.forceSim.force("collide", bubbleCollideForce);
      }
      if (this.force_type == "charge") {
        let bubbleCharge = d => {
          return -Math.pow(d.scaled_radius, 2) * +this.force_strength;
        };
        this.forceSim.force(
          "charge",
          d3.forceManyBody().strength(bubbleCharge)
        );
      }
    },

    showLabels(mode) {
      /*
       * Shows labels for each of the positions in the grid.
       */
      let currentLabels = mode.labels;
      let data = [];
      let groupby = this.gridConfig[this.viewingMode].groupby;
      for (let i = 0; i < currentLabels.length; i++) {
        let t = currentLabels[i];
        let change = d3.sum(
          this.nodes.filter(d => d[groupby] == t),
          d => this.getSpendingDiff(d, false)
        );
        data.push([t, change]);
      }

      let bubble_group_labels = this.innerSVG
        .selectAll(".bubble_group_label")
        .data(data, d => d);

      let grid_element_half_height =
        this.canvasHeight / (mode.gridDimensions.rows * 2);

      let t = d3.transition().duration(1000);

      // remove labels
      bubble_group_labels.exit().remove();

      // update
      let texts = bubble_group_labels
        .enter()
        .append("text")
        .attr("class", "bubble_group_label")
        .attr("text-anchor", "middle")
        .attr("dominant-baseline", "hanging");

      texts
        .merge(bubble_group_labels)
        .attr("x", function(d) {
          return mode.gridCenters[d[0]].x;
        })
        .attr("y", function(d) {
          return mode.gridCenters[d[0]].y - grid_element_half_height;
        })
        .attr("opacity", 0)
        .transition(t)
        .attr("opacity", 1.0);

      texts.append("tspan").text(d => d[0]);

      texts
        .append("tspan")
        .text(d => {
          return netChangeFormatFn(d[1]);
        })
        .attr("class", "bubble_group_sublabel")
        .attr("x", function(d) {
          return mode.gridCenters[d[0]].x;
        })
        .attr("dy", 25)
        .classed("bubble_group_sublabel_positive", d => {
          return d[1] > 0;
        });
    },
    tooltipContent(d) {
      let content = `<div class="tooltip-title">${d.name}</div>
                  <table class="w-100">
                  <tbody>`;

      let sign;

      for (let i = 0; i < this.tooltipConfig.length; i++) {
        let cur_tooltip = this.tooltipConfig[i];
        let value_formatted;
        sign = "";
        if (cur_tooltip.data_field == "diff") {
          sign = d.color_flag == "Down" ? "-" : "+";
        }
        // If a format was specified, use it
        if (d[cur_tooltip.data_field] != undefined) {
          if ("format_string" in cur_tooltip) {
            if (cur_tooltip.data_field == "percent_diff") {
              if (isFinite(d[cur_tooltip.data_field])) {
                value_formatted = d3.format(cur_tooltip.format_string)(
                  d[cur_tooltip.data_field]
                );
              } else {
                value_formatted = "N/A";
              }
            } else if (cur_tooltip.data_field == "actual_radius") {
              value_formatted = netChangeFormatFn(
                d[`${this.fiscalYear} (Revised)`] -
                  d[`${this.fiscalYear} (Proposed)`]
              );
            } else {
              value_formatted = `$${d3
                .format(cur_tooltip.format_string)(d[cur_tooltip.data_field])
                .replace(/G/, "B")}`;
            }
          } else {
            value_formatted = d[cur_tooltip.data_field];
          }

          content += ` <tr class="tooltip-line">
                  <td class="tooltip-line-header">${cur_tooltip.title}</td>
                <td>${sign}${value_formatted}</td>
                </tr>`;
        }
      }
      content += `</tbody>
              </table>`;
      return content;
    },

    showTooltip(d, i, n) {
      /*
       * Function called on mouseover to display the
       * details of a bubble in the tooltip.
       */
      // Change the circle's outline to indicate hover state.
      d3.select(n[i]).attr("stroke", "black");

      // Show the tooltip
      this.tooltip.html(this.tooltipContent(d)).show(d, n[i]);
    },

    hideTooltip(d, i, n) {
      // Reset the circle's outline back to its original color.
      let originalColor = d3
        .rgb(this.fillColorScale(this.getSpendingDiffPercent(d)))
        .darker();
      d3.select(n[i]).attr("stroke", originalColor);

      // Hide the tooltip
      this.tooltip.hide(d, n[i]);
    }
  }
};
</script>

<style>
/* tooltip */
.tooltip-line {
  border-bottom: 1px solid #f0f0f0;
}
.tooltip-line td {
  padding: 0 7px 0 7px;
}
.tooltip-line-header {
  font-weight: bold;
  text-align: left;
}

.tooltip-title {
  margin-bottom: 5px;
  border-bottom: 1px solid #cdcdcd;
  text-align: center;
  font-weight: bold;
  padding-bottom: 5px;
}

.tooltip {
  line-height: 1.2;
  font-weight: 500;
  padding: 12px;
  background: rgba(0, 0, 0, 0.8);
  color: #fff;
  border-radius: 2px;
  border: 2px solid #cfcfcf;
  pointer-events: none;
  background: #fff;
  opacity: 0.9;
  color: black;
  padding: 10px;
  width: 350px;
  font-size: 1rem !important;
}

#toolbar {
  margin-top: 10px;
}

.bubble_group_label {
  font-size: 1.2rem;
  font-weight: 500;
  cursor: default;
  pointer-events: none;
}

.vgt-row-header {
  font-weight: 500;
}
.bubble_group_sublabel {
  fill: #da3b46;
}
.bubble_group_sublabel_positive {
  fill: #398649;
}
</style>