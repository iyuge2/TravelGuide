<template>
  <div>
    <div class="page-header">
      <h1 style="text-align:center">带你去旅行</h1>
    </div>
    <div class="container">
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
              v-model="searchInput"
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
        <contents v-bind:guides="guides" v-bind:searchtext="mysearch" v-bind:isrequest="isRequest"></contents>
        <div class="col-md-1 column" style="text-align: center; font-size: 16px">
        <p>
          <strong>热门推荐</strong>
        </p>
        <div>
        <a v-for="city in hotCity" :key="city" @click="searchHotCity(city)"> <p> {{city}} </p> </a>
        </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
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
      hotCity: ["重庆", "西安", "苏州", "澳门", "青岛", "大连", "昆明", "厦门", "北京", "珠海"],
      MODE: ["综合搜索", "地点搜索", "标题搜索", "概要搜索", "作者搜索"],
      MONTH: ALLMONTH,
      mysearch: "",
      searchInput: "",
      isRequest: true
    };
  },
  props: ["indexSearch"],
  components: {
    contents: contents
  },
  methods: {
    setSearch() {
      this.mysearch = this.searchInput;
    },
    searchHotCity(city) {
      this.mysearch = city;
      this.searchInput = city;
    }
  },
  mounted: function(){
    if(this.indexSearch == ""){ // 优先加载上一个页面传入的搜索词
      this.mysearch = window.localStorage ? localStorage.getItem("mysearch") : "";
      this.searchInput = this.mysearch
    }
    else{ // 若没有搜素词，则根据缓存加载
      this.mysearch = this.indexSearch
      this.searchInput = this.mysearch
    }
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
          param = '{ "query": {"multi_match": { "query": "' + this.mysearch +'",  "fields": ["city_name", "title", "outline"], "type": "best_fields", "tie_breaker":0.3 } }, "size": 5000}'
          break;
        case "地点搜索":
          // param = '{ "query": {"bool": { "must": [{ "match": { "city_name": "'  + this.mysearch +'"} }] }},"size":5000}';
          param = '{ "query": { "match_phrase": { "city_name": "'  + this.mysearch +'"} },"size":5000}';
          break;
        case "标题搜索":
          param = '{ "query": { "match": { "title": "'  + this.mysearch +'" } },"size":5000}';
          break;
        case "概要搜索":
          param = '{ "query": { "match": { "outline": "'  + this.mysearch +'" } },"size":5000}';
          break;
        case "作者搜索":
          // param = '{ "query": {"bool": { "should": [{ "match": { "author": "'  + this.mysearch +'" } }] }},"size":5000}';
          param = '{ "query": { "match": { "author": "'  + this.mysearch +'" } },"size":5000}';
          break;
        default:
          break;
      }
      return param;
    }
  },
  watch: {
    searchParam: function(){
      this.raw_guides = [];
      this.isRequest = true;
      getElasticDate(this.searchParam).then((res) => {
        this.raw_guides = res.data.hits.hits;
        this.isRequest = false;
      })
    },
    mysearch: function(){
      if(window.localStorage){
        localStorage.setItem("mysearch", this.mysearch);
      }
    }
  }
};
</script>

<style>
</style>