<template>
    <div class="comment-list">
      <div v-for="comment in comments" :key="comment.id" class="comment">
        <div class="comment-avatar">
          <img :src="avatar" alt="评论者头像">
        </div>
        <div class="comment-details">
          <div class="comment-header">
            <h3 class="comment-username">{{ comment.username }}</h3>
            <span class="comment-time">{{ formatDate(comment.created_at) }}</span>
            <button @click="deletecomment(comment.id)" class="editbutton">删除</button>
          </div>
          <div class="comment-content">
            <p>{{ comment.content }}</p>
          </div>

          
        </div>
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
import axios from 'axios';
import {ElNotification} from 'element-plus'

export default {
  name: 'Editcomment',
  data() {
    return {
      comment: '',
      comments:[],

      attachment:'',
      attachment_flag:false,

      articleId: this.$store.state.articledetail.id, 
      userId: this.$store.state.userid, 
      avatar:'http://127.0.0.1:5000/static/avatar/default.png',

      currentPage: 1, // 当前页码
      perPage: 10, // 每页显示的记录数
      pageCount: 0, // 总页数
      displayedPages: [], // 显示的页码列表
    };
  },

  mounted() {
    this.getCommentsByPage(this.currentPage); // 页面加载时获取评论列表
  },


  methods: {

    async getCommentsByPage(page) {
      const response = await axios.get(`/api/comments/get/${page}?per_page=${this.perPage}&article_id=${this.articleId}`);
        const {total, comments} = response.data;
        this.comments = comments;
        this.comments.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)); // 对评论数组进行排序
        this.pageCount = Math.ceil(total / this.perPage);
        //更新显示的页码列表
        this.updateDisplayedPages();

    },

    // Search(){
    //   this.changePage(1);
    //   this.getCommentsByPage(this.currentPage);
    // },

    deletecomment(id){
        axios.post('/api/comments/delete', { id:id })
        .then(response => {
          // 删除成功，从页面中移除评论
          console.log(response)
          this.getCommentsByPage(this.currentPage);
          ElNotification({
                title: '文章删除成功！',
                message: '成功删除一条评论✨',
                type: 'success',
              });
        })
        .catch(error => {
          console.error(error);
          ElNotification({
                title: '评论删除失败！',
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
      this.getCommentsByPage(page);
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

.comment-list {
  display: flex;
  flex-wrap: wrap;
}

.comment {
  width: 100%;
  margin-bottom: 20px;
  /* border: 1px solid #ccc; */
  border-bottom: 1px solid #ccc;
  border-radius: 5px;
  display: flex;
  align-items: center;
  padding: 10px;
}

.comment-avatar {
  margin-right: 20px;
}

.comment-avatar img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}

.comment-details {
  flex: 1;
}

.comment-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.comment-username {
  font-size: 18px;
  font-weight: bold;
  margin-right: 10px;
}

.comment-time {
  font-size: 14px;
  color: #666;
}

.comment-content {
  margin-top: 10px;
}

.comment-content p {
  margin: 0;
  font-size: 16px;
  line-height: 1.5;
}

.editbutton {
  background-color: #3de1ad;
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.editbutton:hover {
  background-color: #45a687;
}

</style>