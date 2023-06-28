<template>
    <div>
      <div v-if="loading">加载中...</div>
      <div v-else>
        <div class="search-box">
        <input v-model="searchtext" type="text" placeholder="Search...">
        <button @click="Search" type="submit"><img src="../assets/search.png" alt="Search"></button>
        </div>

        <table>
          <thead>
            <tr>
              <th>标题</th>
              <th>作者</th>
              <th>创作时间</th>
              <th>评论管理</th>
              <th>编辑</th>
              <th>删除</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="article in articles" :key="article.id">
              <td>{{ article.title }}</td>
              <td>{{ article.username }}</td>
              <td>{{ formatDate(article.created_at )}}</td>
              <td>
                
                <router-link to="/Editcomment">
                <button @click="()=>{this.$store.commit('setarticledetail', article)}" >评论管理</button>
                </router-link>

            </td>
              <td>
                <router-link to="/Update">
                <button @click="()=>{this.$store.commit('setarticledetail', article)}">编辑</button>
                </router-link>
              </td>
              <td>
                <button @click="deletearticle(article)">删除</button>
              </td>
            </tr>
          </tbody>
        </table>

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
    </div>
  </template>
  
  <script>
  import axios from 'axios';
//   import {ElMessageBox} from 'element-plus'
 import {ElNotification} from 'element-plus'
  
  export default {
    name:'Edit',
    components: {

    },
    data() {
      return {
        loading: true,
        articles: [],
       
        currentPage: 1, // 当前页码
        perPage: 15, // 每页显示的记录数
        pageCount: 0, // 总页数
        displayedPages: [], // 显示的页码列表

        searchtext:'',

        // deleteflag:0,
      };
    },
    created() {
      this.getArticlesByPage(this.currentPage);
    },
    methods: {
    // 获取指定页码的文章列表
    async getArticlesByPage(page) {
      const response = await axios.get(`/api/articlesedit/page/${page}?per_page=${this.perPage}&searchtext=${this.searchtext}`);
      const { total, articles } = response.data;
      // console.log(articles)
      // 更新文章列表和总页数
      this.articles = articles;
      this.pageCount = Math.ceil(total / this.perPage);
      console.log(response);
      // 更新显示的页码列表
      this.updateDisplayedPages();
      this.loading = false;
      
    },

    Search(){
      this.changePage(1);
      this.getArticlesByPage(this.currentPage);
    },


    // 删除
    deletearticle(article){
    //     ElMessageBox.confirm('确认删除这篇文章吗?')
    // .then(() => {
    //     this.deletesend(article);
    // })
    // .catch(() => {
    //     console.log('放弃删除')
    // })
    
    this.deletesend(article)
    },

    deletesend(article){
              // 发送 POST 请求来删除文章
      axios.post('/api/delete-article', { 
        articleId: article.id 
    })
        .then(response => {
          console.log(response.data); // 打印响应数据
          console.log('删除成功');
          this.getArticlesByPage(this.currentPage);
          ElNotification({
                title: '文章删除成功！',
                message: '成功删除一篇文章✨',
                type: 'success',
              });
        })
        .catch(error => {
          console.log(error);
          ElNotification({
                title: '文章删除失败！',
                message: '请检查您的网络连接并重试',
                type: 'error',
              });
        });
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

    formatDate(dateStr) {
        const date = new Date(dateStr)
        const year = date.getFullYear()
        const month = date.getMonth() + 1
        const day = date.getDate()
        return `${year}-${month}-${day}`
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

    watch: {
    currentPage() {
      this.updateDisplayedPages();
    },
    pageCount() {
      this.updateDisplayedPages();
    },
  },

    },
  };
  </script>

  <style>
  .search-box{
    margin-bottom: 10px;
    margin-left: 100px;
  }
    table {
  border-collapse: collapse;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}

thead {
  background-color: #f2f2f2;
}

th,
td {
  padding: 12px;
  text-align: left;
  border: 1px solid #ddd;
}

th {
  font-weight: bold;
}

tr:hover {
  background-color: #f5f5f5;
}

td button {
  background-color: #3de1ad;
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

td button:hover {
  background-color: #45a687;
}
  </style>