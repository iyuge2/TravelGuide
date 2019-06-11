<template>
  <div>
    <div class="page-header">
      <h1 style="text-align:center">带你去旅行</h1>
    </div>
    <div class="container">
      <search @startSearch="getSearch" v-bind:searchfor="mysearch"></search>
      <br>
      <div class="row clearfix">
        <div class="col-md-2 column">
          <!-- 搜索方式 -->
          <p>
            <strong>搜索方式</strong>
          </p>
          <select class="btn btn-defaul" v-model="choose.searchMode">
            <option v-for="i in MODE" :key="i">{{i}}</option>
          </select>
          <br>
          <br>
          <!-- 选择排序 -->
          <p>
            <strong>排序方式</strong>
          </p>
          <div class="radio">
              <label>
                <input type="radio" name="optionsRadios" value="综合排序" v-model="choose.sortMode" checked>
                综合排序
              </label>
          </div>
          <div class="radio">
              <label>
                <input type="radio" name="optionsRadios" value="最近出发" v-model="choose.sortMode">
                最近出发
              </label>
          </div>
          <div class="radio">
              <label>
                <input type="radio" name="optionsRadios" value="热度最高" v-model="choose.sortMode">
                热度最高
              </label>
          </div>
          <br>
          <p>
            <strong>选择出行天数</strong>
          </p>
          <input type="text" v-model.number="choose.daysBegin" style="width: 40px">
          <span> --- </span>
          <input type="text" v-model.number="choose.daysEnd" style="width: 40px">
          <!-- <textarea>---</textarea> -->
          <br>
          <br>

          <p>
            <strong>选择出行月份</strong>
          </p>
          <select class="btn btn-defaul" v-model="choose.monthBegin">
            <option v-for="i in MONTH.slice(0, choose.monthEnd)" :key="i">{{i}}</option>
          </select>
          <span> --- </span>
          <!-- <textarea>---</textarea> -->
          <select class="btn btn-defaul" v-model="choose.monthEnd">
            <option v-for="i in MONTH.slice(choose.monthBegin-1, 12)" :key="i">{{i}}</option>
            
          </select>
        </div>
        <contents v-bind:guides="guides" v-bind:searchtext="mysearch"></contents>
        <div class="col-md-1 column"></div>
      </div>
    </div>
  </div>
</template>

<script>
import searchBox from "./SearchBox.vue";
import contents from "./Contents.vue";
import axios from "axios";

axios.defaults.headers.post["Content-Type"] = "application/json";
let base = '/api/_search';

const getElasticDate = params => {
  return axios.post(`${base}`, params);
};

function compare(property){
  return function(obj1,obj2){
    if(property == "score"){
      return obj2._score - obj1._score;
    }
    else{
      var value1 = obj1._source[property];
      var value2 = obj2._source[property];
      // 降序
      if(property == "date"){
        var date1 = new Date(value1);
        var date2 = new Date(value2);
        return date2.getTime() - date1.getTime();
      }
      else{
        return value2 - value1;     
      }
    }
  }
}

const ALLMONTH = [];
for(let i = 0; i < 12; i++){
  ALLMONTH.push(i+1);
}

export default {
  name: "page2Root",
  data() {
    return {
      raw_guides: [],
      choose: {
        searchMode: "综合搜索",
        sortMode: "综合排序",
        daysBegin: 0,
        daysEnd: 1000,
        monthBegin: 1,
        monthEnd: 12
      },
      MODE: ["综合搜索", "地点搜索", "标题搜索", "概要搜索", "作者搜索"],
      // MODE: ["综合搜索"],
      MONTH: ALLMONTH,
      mysearch: ""
    };
  },
  props: ["searchcontent"],
  components: {
    search: searchBox,
    contents: contents
  },
  methods: {
    getSearch(msg) {
      this.mysearch = msg;
    }
  },
  mounted: function(){
    this.mysearch = this.searchcontent
  },
  computed:{
    guides: function(){
      var guides_tmp = this.raw_guides;
      var daysbegin = this.choose.daysBegin;
      var daysend = this.choose.daysEnd;
      var monthbegin = this.choose.monthBegin;
      var monthend = this.choose.monthEnd;
      // if(daysend < daysbegin){
      //   alert("出行天数设置异常，左边的值不能大于右边的值");
      // }
      guides_tmp = guides_tmp.filter(function(item){
        if(item._source.days == -1){
          return true;
        }
        return item._source.days >= daysbegin & item._source.days <= daysend;
      });
      guides_tmp = guides_tmp.filter(function(item){
        if(item._source["date"] == "1972-01-01"){
          return true;
        }
        var cur_month = parseInt(item._source["date"].split("-")[1]);
        return cur_month >= monthbegin & cur_month <= monthend;
      });
      switch(this.choose.sortMode){
        case "热度最高":
          guides_tmp.sort(compare("view")); 
          break;
        case "最近出发":
          guides_tmp.sort(compare("date")); 
          break;
        case "综合排序":
          guides_tmp.sort(compare("score"));
          break;
        default:
          break;
      }
      return guides_tmp;
    },
    searchParam: function(){
      let param = "";
      switch(this.choose.searchMode){
        case "综合搜索":
          param = '{ "query": {"bool": { "must": [{ "match": { "city_name": "'+this.mysearch+'" } }, { "match": { "title": "'  + this.mysearch +'" } }, { "match": { "outline": "' + this.mysearch + '" } }], "should": [ {"match": {"outline": "' + this.mysearch + '"}}] }},"size":10000}';
          break;
        case "地点搜索":
          param = '{ "query": {"bool": { "must": [{ "match": { "city_name": "'  + this.mysearch +'" } }] }},"size":10000}';
          break;
        case "标题搜索":
          param = '{ "query": {"bool": { "should": [{ "match": { "title": "'  + this.mysearch +'" } }] }},"size":10000}';
          break;
        case "概要搜索":
          param = '{ "query": {"bool": { "should": [{ "match": { "outline": "'  + this.mysearch +'" } }] }},"size":10000}';
          break;
        case "作者搜索":
          param = '{ "query": {"bool": { "should": [{ "match": { "author": "'  + this.mysearch +'" } }] }},"size":10000}';
          break;
        default:
          break;
      }
      return param;
    }
  },
  watch: {
    searchParam: function(){
      getElasticDate(this.searchParam).then((res) => {
        this.raw_guides = res.data.hits.hits;
      });
    }
  }
};
</script>

<style>
</style>