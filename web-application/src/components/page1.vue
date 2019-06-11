<template>
  <div class="searchbox col-md-6 column">
      <div class="input-group">
        <input
          type="text"
          class="form-control"
          v-model="searchtext"
          @change="search"
          placeholder="国内城市/国内景点/..."
        >
        <span class="input-group-btn">
          <button class="btn btn-default" type="button" @change="search">
            <span class="glyphicon glyphicon-zoom-out" aria-hidden="true"></span>
          </button>
        </span>
      </div>
  </div>
</template>

<script>
// backgroundImg: require('../assets/back.jpeg');

export default {
  name: "page1Root",
  data() {
    return {
      searchtext: ""
    };
  },
  methods: {
    search: function() {
      this.$router.push("/results");
      this.$emit("startSearch", this.searchtext);
    },
  },
  beforeCreate: function(){
    document.body.style.backgroundImage = "url(./img/back.jpg)";
  },
  beforeDestroy: function(){
    document.body.style.backgroundImage = "";
  }
}
</script>

<style>
.searchbox {
  position: absolute;
  top: 150px;
  left: 200px;
}
</style>