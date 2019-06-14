<template>
  <div class="row clearfix">
    <!-- logo -->
    <div class="col-md-2 column">
      <a href="/">
        <img src="../assets/go.jpg" class="img-circle" width="34px" style="float: right">
      </a>
    </div>
    <!-- 搜索框 -->
    <div class="col-md-6 column">
      <div class="input-group" @keyup.enter="setSearch">
        <input
          type="text"
          class="form-control"
          v-model="searchtext"
          placeholder="国内城市/国内景点/..."
        >
        <span class="input-group-btn">
          <button class="btn btn-default" type="button" @click="setSearch">
            <span class="glyphicon glyphicon-zoom-out" aria-hidden="true"></span>
          </button>
        </span>
      </div>
    </div>
    <div class="col-md-4 column"></div>
  </div>
</template>

<script>
export default {
  name: "Searchbox",
  data() {
    return {
      searchtext: ""
    };
  },
  props: ['searchfor'],
  updated: function(){
    this.searchtext = this.searchfor;
  },
  methods: {
    setSearch: function() {
      this.$emit("startSearch", this.searchtext);
    }
  }
};
</script>

<style type="text/css">
.searchbox {
  position: absolute;
  top: 150px;
  left: 200px;
}
</style>

