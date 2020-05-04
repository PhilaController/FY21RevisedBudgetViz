<template>
  <div class="btn-group" role="group">
    <button
      class="btn btn-primary dropdown-toggle w-100"
      type="button"
      data-toggle="dropdown"
      aria-haspopup="true"
      aria-expanded="false"
    >{{displayedValue}}</button>
    <div class="dropdown-menu header-dropdown-menu">
      <a
        v-for="item in items"
        :key="item.id"
        class="dropdown-item"
        @click="handleClick(item.id)"
      >{{item.text}}</a>
    </div>
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
  watch: {
    options(newOptions, oldOptions) {
      let oldSelectedValue = oldOptions[this.selectedOption];
      let index = newOptions.indexOf(oldSelectedValue);
      if (index != -1) this.selectedOption = index;
    }
  },
  methods: {
    handleClick: function(i) {
      if (i !== this.selectedOption) {
        this.selectedOption = i;
        this.$emit("change", this.options[i]);
      }
    }
  }
};
</script>
