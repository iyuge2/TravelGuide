<template>
  <!-- 搜索内容展示 -->
  <div class="col-md-9 column">
    <p v-if="guides.length == 0">很抱歉，没有找到与<strong style="color: red">"{{searchtext}}"</strong>相关的结果<br>
    请检查<strong style="color: red">搜索条件</strong>或者<strong style="color: red">换一个搜索句</strong>进行搜索...</p>
    <p v-if="guides.length != 0">共 {{page_num}} 页, {{guides.length}}个结果</p>
    <ul class="list-group">
      <!-- <li class="list-group-item" style="width: 800px"> -->
      <li class="list-group-item" v-for="cur_guide in guides.slice(start_num,end_num)">
        <div class="row">
        <div>
          <!-- 第一张图片 -->
          <div class="col-md-4 column">
            <a v-bind:href="cur_guide._source.guide_url" target="_blank">
              <img :src="cur_guide._source.cover_img_url" width="250px" height="150px">
            </a>
          </div>
          <div class="col-md-8">
            <div class="caption">
              <!-- title -->
              <h3>
                <a :href="cur_guide._source.guide_url" target="_blank">{{cur_guide._source.title}}</a>
              </h3>
              <!-- author + date + length -->
              <h6>
                <span class="glyphicon glyphicon-user" aria-hidden="true">
                  <a :href="cur_guide._source.author_url" target="_blank"> {{cur_guide._source.author}} </a>
                </span>
                <span v-if="cur_guide._source.date != '1972-01-01'"> {{cur_guide._source.date}} 出发 |</span>
                <span v-if="cur_guide._source.days != -1"> 共 {{cur_guide._source.days}} 天 </span>
                <span class="glyphicon glyphicon-thumbs-up" aria-hidden="true" style="float: right; color: red">  {{cur_guide._score}} </span>
              </h6>
              <!-- content -->
              <p>{{cur_guide._source.outline}}</p>
              <!-- city_name -->
              <span
                class="glyphicon glyphicon-map-marker"
                aria-hidden="true"
              > {{cur_guide._source.city_name}}</span>
              <span
                class="glyphicon glyphicon-eye-open"
                aria-hidden="true"
                style="float: right"
              > {{cur_guide._source.view}}</span>
            </div>
          </div>
        </div>
        </div>
      </li>
    </ul>
    <div style="text-align: center">
      <ul class="pagination">
        <li>
          <a @click="pageFirst" v-if="cur_page_num > 1"> 首页 </a>
        </li>
        <li>
          <a @click="pageDown" v-if="cur_page_num > 1"> 上一页 </a>
        </li>
        <li v-for="i in pages" :key="i">
          <a @click="pageAt(i)" v-bind:style="{color: (i==cur_page_num) ? 'red': '#337ab7'}"> {{i}} </a>
        </li>
        <li>
          <a @click="pageUp" v-if="cur_page_num != page_num"> 下一页 </a>
        </li>
        <li>
          <a @click="pageLast" v-if="cur_page_num != page_num"> 末页 </a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
const ITEMS_PER_PAGE = 10;
export default {
  name: "contents",
  data() {
    return {
      cur_page_num: 0 //当前第几页
    };
  },
  props: ["guides", "searchtext"],
  computed: {
    page_num: function(){ // 攻略总页数
      return Math.round(this.guides.length / ITEMS_PER_PAGE);
    },
    left_page: function(){ // 最左边一页的编号
      return (this.cur_page_num - 4 >= 1) ? this.cur_page_num - 4 : 1;
    },
    right_page: function(){ // 最右边一页的编号
      return (this.left_page + 8 <= this.page_num) ? this.left_page + 8 : this.page_num;
    },
    pages: function(){ // 页数编号
      var tmp = [];
      for(var j = this.left_page; j <= this.right_page; j++){
        tmp.push(j);
      }
      return tmp
    },
    start_num: function(){ // 当前展示的攻略页第一条是第几项 
      return (this.cur_page_num - 1) * ITEMS_PER_PAGE;
    },
    end_num: function(){ // 当前展示的攻略页最后一条是第几项
      return (this.cur_page_num == this.page_num) ? this.guides.length-1 : this.start_num + ITEMS_PER_PAGE;
    }
  },
  methods:{
    pageDown: function(){
      if(this.start_num - ITEMS_PER_PAGE >= 0){
        this.cur_page_num -= 1;
      }
    },
    pageUp: function(){
      if(this.end_num + ITEMS_PER_PAGE <= this.guides.length){
        this.cur_page_num += 1;
      }
    },
    pageAt: function(i){
      this.cur_page_num = i;
    },
    pageFirst: function(){
      this.cur_page_num = 1;
    },
    pageLast: function(){
      this.cur_page_num = this.page_num;
    }
  },
  watch:{
    guides: function(){
      if(this.guides.length){
        this.cur_page_num = 1;
      }
      else{
        this.cur_page_num = 0;
      }
    }
  }
};
</script>
<style>
</style>
