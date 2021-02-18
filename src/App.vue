<template>
  <div id="app">
    <div id="nav">
      <router-link to="/" class="my-nav-link">Home</router-link>
      <router-link to="/spending" class="my-nav-link">Spending</router-link>
      <router-link to="/revenue" class="my-nav-link">Revenue</router-link>
      <router-link to="/guide" class="my-nav-link">Guide</router-link>
    </div>
    <transition name="fade" mode="out-in">
      <keep-alive>
        <router-view :key="$route.path" />
      </keep-alive>
    </transition>
  </div>
</template>

<script>
export default {
  name: "app",
  components: {},
  created() {
    // IMPORTANT: make sure FA does not watch SVG elements
    if (window.FontAwesome) {
      window.FontAwesome.config.observeMutations = false;
      window.FontAwesome.config.searchPseudoElements = false;
    }
  },
};
</script>

<style>
@media only screen and (max-width: 736px) {
  .header-button-block {
    width: 100%;
  }
}
@media only screen and (min-width: 736px) {
  .entry-header .row:first-child {
    flex-wrap: nowrap;
  }
}
.fade-enter-active,
.fade-leave-active {
  transition-duration: 0.3s;
  transition-property: opacity;
  transition-timing-function: ease;
}
.fade-enter,
.fade-leave-active {
  opacity: 0;
}
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#nav {
  padding: 30px;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
#nav a {
  font-weight: bold;
  font-size: 1.2rem;
}
.my-nav-link:not(:last-child) {
  border-right: 2px solid #666;
  padding-right: 0.25rem;
}
.my-nav-link:not(:first-child) {
  padding-left: 0.25rem;
}
.my-nav-link:hover {
  text-decoration: none;
}
#nav a.router-link-exact-active {
  color: #f3c613 !important;
}
#nav a,
.my-nav-link {
  color: #2176d2 !important;
}
.my-nav-link:hover {
  color: #0f4d90 !important;
}
.my-card-title {
  font-size: 1.5rem;
  font-weight: 500;
}
.text-link:hover {
  text-decoration: none;
}
.text-link {
  color: #2176d2 !important;
}
.text-link:hover {
  color: #0f4d90 !important;
}
</style>
