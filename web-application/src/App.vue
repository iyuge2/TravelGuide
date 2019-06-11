<template>
  <div id="app">
    <router-view @startSearch="getSearch" v-bind:searchcontent="searchtext"></router-view>
    <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
  </div>
</template>

<script>
export default {
  name: "app",
  data() {
    return {
      searchtext: ""
    };
  },
  methods: {
    getSearch(msg) {
      this.searchtext = msg;
    }
  }
};
</script>

<style>

</style>
