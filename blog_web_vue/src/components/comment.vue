<template>
    <hr>
    <div v-if="this.attachment_flag" class="attachment">
      <div class="attachment-card-text">
        <img class="file_image" src="../assets/file.png" alt="file icon">
        <p class="file_name">{{ attachment.filename }}</p>
        <a :href="attachment.path" download class="attachment-download-btn">下载</a>
      </div>
    </div>
    <div class="clear"></div>
    <hr>
    <div v-if="this.$store.state.isLoggedIn" class="comment-form">
      <form @submit.prevent="submitComment">
        <textarea v-model="comment" placeholder="善语结善缘，恶语伤人心"></textarea>
        <button type="submit">提交评论</button>
      </form>
    </div>
    <hr>
    <!-- <div class="comments">
      <h3>评论列表</h3>
      <ul>
        <li v-for="comment in comments" :key="comment.id">
          <p>{{ comment.content }}</p>
          <p>{{ comment.username }}</p>
          <p>{{ comment.created_at }}</p>
        </li>
      </ul>
    </div> -->

    <div class="comment-list">
      <div v-for="comment in comments" :key="comment.id" class="comment">
        <div class="comment-avatar">
          <img :src="avatar" alt="评论者头像">
        </div>
        <div class="comment-details">
          <div class="comment-header">
            <h3 class="comment-username">{{ comment.username }}</h3>
            <span class="comment-time">{{ formatDate(comment.created_at) }}</span>
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

<style>
.file_image{
  width: 40px;
  height: 40px;
  vertical-align: middle;
}
.attachment-card-text{
  display: flex;
  align-items: center;
}
.file_name{
 margin-right: 10px;
}

.attachment-card-text a{
  color: #3de1ad;
}
.attachment-card-text a:hover{
  color: #1dd198;
}

.comment-form {
  width: 90%;
  margin-top: 20px;
  margin: 0 auto;
  /* border: 1px solid #ccc; */
  padding: 10px;
}

.comment-form textarea {
  width: 90%;
  height: 100px;
  font-size: 16px;
  padding: 10px;
  /* border: 1px solid #ccc; */
  border-radius: 5px;
  resize: none;
}

.comment-form button {
  display: block;
  width: 150PX;
  margin-top: 10px;
  padding: 10px 20px;
  font-size: 16px;
  background-color: #3de1ad;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.comment-form button:hover {
  background-color: #73f4cb;
}





hr{
  border: 1px solid #ccc;
}

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

</style>

<script>
import axios from 'axios';
import {ElNotification} from 'element-plus'

export default {
  name: 'Comment',
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
    this.getAttachments(); //页面加载时获取附件列表
    this.getCommentsByPage(this.currentPage); // 页面加载时获取评论列表
  },


  methods: {
    // 获取指定文章的所有附件
    getAttachments() {
       axios.post('/api/article/getattachments', {
        article_id: this.articleId,
       })
       .then(response => {
        console.log(response.data.attachments);
        this.attachment = response.data.attachments[0];
        this.attachment_flag = response.data.success;
        console.log(this.attachment.path);
        
       })
       .catch(error => {
        console.error(error)
        return []
       })
    },

    submitComment() {
      axios.post('/api/comments/submission', {
          content: this.comment,
          user_id: this.userId,
          article_id: this.articleId,
        })
        .then(response => {
          console.log(response.data);
          this.getCommentsByPage(this.currentPage); // 发布成功后刷新评论列表
          ElNotification({
              title: '成功！',
              message: '发布了一条新的评论🎈',
              type: 'success',
              })
        })
        .catch(error => {
          console.log(error);
          ElNotification({
              title: '失败！',
              message: '发布评论遇到了问题🧱',
              type: 'error',
              })
        });
    },

    async getCommentsByPage(page) {
      const response = await axios.get(`/api/comments/get/${page}?per_page=${this.perPage}&article_id=${this.articleId}`);
      // , {
      //     params: {
      //       article_id: this.articleId,
      //     },
      //   })
        // .then(response => {
        //   console.log('返回结果:',response.data);
        //   this.comments = response.data; // 更新评论数组的值
        //   this.comments.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)); // 对评论数组进行排序
        // })
        // .catch(error => {
        //   console.log(error);
        // });
        const {total, comments} = response.data;
        this.comments = comments;
        this.comments.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)); // 对评论数组进行排序
        this.pageCount = Math.ceil(total / this.perPage);
        //更新显示的页码列表
        this.updateDisplayedPages();

    },

    Search(){
      this.changePage(1);
      this.getCommentsByPage(this.currentPage);
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

    // 格式化日期
    // formatDate(dateString) {
    // const date = new Date(dateString);
    // return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()} ${date.getHours()}:${date.getMinutes()}`;
    // },
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