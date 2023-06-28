<template>
  <div class="web_header">
  <div class="card-nav">
  <a href="#" class="card-nav-item active">最热</a>
  <a href="#" class="card-nav-item">最新</a>
  <a href="#" class="card-nav-item">关注</a>
</div>

<div class="search-box">
  <input v-model="searchtext" type="text" placeholder="Search...">
  <button @click="Search" type="submit"><img src="../assets/search.png" alt="Search"></button>
</div>
</div>

  <div class="article-list">
    <!-- 显示文章列表 -->
    
    <div class="listcard" v-for="article in articles" :key="article.id">
      <router-link to="/ArticleDetails">
      <div @click="()=>{this.$store.commit('setarticledetail', article)}" class="listcard-body">
        <h3 class="listcard-title">{{ article.title }} <Tag :label="article.category_name" type="success"></Tag>  <Tag label="管理员" type="primary" v-if="article.title == '标签测试-'"></Tag></h3>
        <div class="listcard-subtitle">
          <span>作者: {{ article.username }}</span>
          <!-- <span>{{ article.created_at }}</span> -->
          <!-- <span>{{ article.category }}</span> -->
          <span>日期: {{ formatDate(article.created_at) }}</span>
        </div>
        <!-- <img v-if="article.imageurl" :src="article.imageurl" alt="文章图片" class="article-image"/> -->
        <div class="image-container" :style="{ backgroundImage: 'url(' + article.imageurl + ')' }"></div>
        <div class="listcard-text">{{ truncate(article.content, 50) }}</div>
      </div>
      <div class="clear"></div>
      <div class="listcard-footer">
        <div class="listcard-footer-item">
          <img src="../assets/shoucang1.png" alt="收藏">
          <span class="footer-text">#</span>
        </div>

        <div class="listcard-footer-item">
          <img src="../assets/pinlun.png" alt="评论">
          <span class="footer-text">{{article.count_all_comment}}</span>
        </div>
  
        <div class="listcard-footer-item">
          <img src="../assets/zan1.png" alt="点赞">
          <span class="footer-text">{{article.count_all_like}}</span>
        </div>
      </div>
      </router-link>
    </div>
  
    <!-- 显示分页导航 -->
    <ul class="pagination">
      <li class="page-item" v-if="currentPage > 1">
        <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">上一页</a>
      </li>
      <li class="page-item" v-for="page in displayedPages" :key="page" :class="{ active: page === currentPage }">
        <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
      </li>
      <li class="page-item" v-if="currentPage < pageCount">
        <a class="page-link" href="#" @click.prevent="changePage(currentPage + 1)">下一页</a>
      </li>
      <li class="page-item disabled">
        <a class="page-link" href="#">{{ currentPage }} / {{ pageCount }}</a>
      </li>
    </ul>
  </div>
</template>

<script>
import '../assets/css/Home.css'
import axios from 'axios';
import Tag from '@/components/tag.vue'



export default {
  name: 'Home',
  data() {
    return {
      articles: [], // 文章列表
      currentPage: 1, // 当前页码
      perPage: 6, // 每页显示的记录数
      pageCount: 0, // 总页数
      displayedPages: [], // 显示的页码列表

      searchtext:''
    };
  },
  mounted() {
    this.getArticlesByPage(this.currentPage);
  },
  components:{
    Tag,

  },

  methods: {
    // 获取指定页码的文章列表
    async getArticlesByPage(page) {
      // 发起异步HTTP请求，从后端API获取文章列表和总记录数
      // if(this.searchtext !=''){
      //   this.changePage(1);
      // }
      const response = await axios.get(`/api/articles/page/${page}?per_page=${this.perPage}&searchtext=${this.searchtext}`);
      const { total, articles } = response.data;
      // console.log(articles)
      // 更新文章列表和总页数
      this.articles = articles;
      this.pageCount = Math.ceil(total / this.perPage);
      // 更新显示的页码列表
      this.updateDisplayedPages();
    },

    Search(){
      this.changePage(1);
      this.getArticlesByPage(this.currentPage);
    },

    // 切换页码
    changePage(page) {
      if (page < 1) {
        page = 1;
      } else if (page > this.pageCount) {
        page = this.pageCount;
      }
      this.currentPage = page;
      this.getArticlesByPage(page);
    },
    // 格式化日期
    formatDate(dateString) {
      const date = new Date(dateString);
      return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
    },
    // 截取字符串
    truncate(text, length) {
      var temphtml = document.createElement('div');
      temphtml.innerHTML = text
      text = temphtml.textContent
      if (text.length <= length) {
        return text;
      }
      return text.substr(0, length) + '...';
    },
    // 更新显示的页码列表
    updateDisplayedPages() {
      const maxDisplayedPages = 5; // 最多显示的页码数
      const halfDisplayedPages = Math.floor(maxDisplayedPages / 2); // 显示页码数的一半
      let startPage = Math.max(1, this.currentPage - halfDisplayedPages);
      let endPage = Math.min(this.pageCount, startPage + maxDisplayedPages - 1);
      if (endPage - startPage + 1 < maxDisplayedPages) {
        endPage = Math.min(maxDisplayedPages, this.pageCount);
        startPage = Math.max(1, endPage - maxDisplayedPages + 1);
      }
      const displayedPages = [];
      for (let i = startPage; i <= endPage; i++) {
        displayedPages.push(i);
      }
      this.displayedPages = displayedPages;
    },
  },
  watch: {
    currentPage() {
      this.updateDisplayedPages();
    },
    pageCount() {
      this.updateDisplayedPages();
    },
  },
};
</script>