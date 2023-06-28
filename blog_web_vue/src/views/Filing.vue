<template>
    <div v-show="!this.flag">
      <div class="category-list">
        <div  @click="getArticlesByCategory(1,category.id)" v-for="category in categorys" :key="category.id" class="category-card" >
          <h3>{{ category.name }}</h3>
          <p>{{ category.description }}</p>
        </div>
      </div>
    </div>

    <div v-show="this.flag" class="articles-list">
    <p class="back" @click="back()">返回</p>
    <ul>
      <li v-for="article in articles" :key="article.id">
        <router-link to="/ArticleDetails">
        <p @click="()=>{this.$store.commit('setarticledetail', article)}">{{ article.title }}  作者: {{ article.username }}  {{formatDate(article.created_at)}}</p>
        </router-link>
    </li>
    </ul>

    
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

    <div class="category-article-list"></div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name:'Filing',
    data() {
      return {
        flag:false,
        categorys: [],
        articles:[],
        categoryId:'',

        currentPage: 1, // 当前页码
        perPage: 15, // 每页显示的记录数
        pageCount: 0, // 总页数
        displayedPages: [], // 显示的页码列表
      };
    },
    mounted() {

        axios.get('/api/getcategory')
        .then(response => {
            this.categorys = response.data.categorys;
            })
        .catch(error => {
          console.error(error);
        });

 
    },

    methods: {
        back(){
            this.flag = false;
        },
        async getArticlesByCategory(page,categoryId) {
            this.flag = true;
            this.categoryId = categoryId;
            const response = await axios.get(`/api/articles/getbycategory/${page}?per_page=${this.perPage}&category_id=${this.categoryId}`);
            const {total, articles} = response.data;
            this.articles = articles;
            this.pageCount = Math.ceil(total / this.perPage);
            //更新显示的页码列表
            this.updateDisplayedPages();
        },

        Search(){
      this.changePage(1);
      this.getArticlesByCategory(this.currentPage,this.categoryId);
    },

    // 切换页码
    changePage(page) {
      if (page < 1) {
        page = 1;
      } else if (page > this.pageCount) {
        page = this.pageCount;
      }
      this.currentPage = page;
      this.getArticlesByCategory(page,this.categoryId);
    },

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString('zh', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          hour12: false,
          timeZone: 'GMT' 
        });
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
  
  <style>
  .back{
    margin: 0;
    padding: 0;
    list-style: none;
    color: #3de1ad;
  }
  .category-list {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
  }
  
  .category-card {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 30%;
    margin: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 10px;
  }

  .category-card p{
    color: #777777;
    margin-left: 10px;
  }

  .category-list h3{
    color: #3de1ad;
  }

  .articles-list {
  text-align: center;
  }

  ul,li p{
  margin: 0;
  padding: 0;
  list-style: none;
  color: #3de1ad;
  margin-top: 5px;
  font-size: 20px;
  }
  
  </style>