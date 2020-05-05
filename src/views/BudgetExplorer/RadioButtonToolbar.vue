<template>
  <div
    class="radio-toolbar-wrapper btn-group btn-group-toggle d-flex justify-content-center"
    data-toggle="buttons"
  >
    <label
      class="btn btn-primary"
      v-for="item in items"
      v-bind:class="{ active: isActive(item.id) }"
      :key="item.id"
      @click="handleClick(item.id)"
    >
      <input type="radio" name="options" v-bind:class="{ checked: isActive(item.id) }" />
      {{ item.text }}
    </label>
  </div>
</template>

<script>
export default {
  props: ["options", "defaultValue"],
  data: function() {
    return {
      selectedOption: null
    };
  },
  created: function() {
    this.selectedOption = this.options.indexOf(this.defaultValue);
    this.$emit("change", this.displayedValue);
  },
  computed: {
    displayedValue: function() {
      return this.options[this.selectedOption];
    },
    items: function() {
      let items = [];
      for (let i = 0; i < this.options.length; i++) {
        items.push({ id: i, text: this.options[i] });
      }
      return items;
    }
  },
  methods: {
    isActive(i) {
      return i == this.selectedOption;
    },
    handleClick: function(i) {
      if (i !== this.selectedOption) {
        this.selectedOption = i;
        this.$emit("change", this.options[i]);
      }
    }
  }
};
</script>

<style scoped>
.btn-primary {
  background-color: #2176d2 !important;
  border-color: #2176d2 !important;
}
.active {
  background-color: #0f4d90 !important;
  border-color: #0f4d90 !important;
}
@media screen and (max-width: 768px) {
  .radio-toolbar-wrapper {
    flex-wrap: wrap;
  }
  .radio-toolbar-wrapper > label {
    width: 165px;
  }
}
</style>

