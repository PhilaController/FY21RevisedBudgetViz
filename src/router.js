import Vue from "vue";
import Router from "vue-router";
import Home from "@/views/Home";
import Spending from "@/views/Spending";
import Revenue from "@/views/Revenue";

Vue.use(Router);

export default new Router({
  scrollBehavior(to, from, savedPosition) {
    return { x: 0, y: 0 };
  },
  routes: [
    {
      path: "/",
      name: "home",
      component: Home
    },
    {
      path: "/spending",
      component: Spending
    },
    {
      path: "/revenue",
      component: Revenue
    },
  ]
});
