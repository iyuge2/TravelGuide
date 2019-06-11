import Vue from "vue";
import App from "./App.vue";
import Page1Root from "./components/page1.vue";
import Page2Root from "./components/page2.vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);
// Vue.use(AsyncComputed);
Vue.config.productionTip = false;


const routes = [
  { path: "/", component: Page1Root },
  { path: "/results", component: Page2Root }
];

const router = new VueRouter({
  routes // (缩写) 相当于 routes: routes
});

new Vue({
  router,
  render: h => h(App)
}).$mount("#app");
