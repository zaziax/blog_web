<template>
    <div class="article-details">
      <div class="top-bar">
        <button class="back-button" @click="goTo('/')">
          <img class="icon" src="../assets/home.png" alt="返回" >
        </button>
      </div>
      <h1>{{ article.title }}</h1>
      <div class="article-meta">
        <span>作者：{{ article.username }}</span>
        <span>分类：{{ article.category_name }}</span>
        <span>日期：{{ formatDate(article.created_at) }}</span>
      </div>

      <img v-if="article.imageurl" :src="article.imageurl" alt="文章图片" class="article-image"/>
      <!-- <div class="article-image" :style="{ backgroundImage: 'url(' + article.imageurl + ')' }"></div> -->

      <div class="article-content" v-html="article.content"></div>
      <div class="clear"></div>
      <div v-if="this.$store.state.isLoggedIn" class="article-actions">
        <button class="action-button" @click="toggleFavorite">
          <img class="icon"  v-if="!isFavorite" src="../assets/shoucang1.png" alt="" srcset="">
          <img class="icon"  v-else src="../assets/shoucang2.png" alt="" srcset="">

        </button>
        <button class="action-button" @click="toggleLike">
          <img class="icon"  v-if="!isLiked" src="../assets/zan1.png" alt="" srcset="">
          <img class="icon"  v-else src="../assets/zan2.png" alt="" srcset="">
        </button>
      </div>

    <div v-if="!this.$store.state.isLoggedIn">
      <h2>请登录以使用完整功能！</h2>
    </div>

    <Comment></Comment>

      <div class="scroll-buttons">
        <button class="scroll-button" @click="scrollToTop">
            <img class="icon"  src="../assets/up.png" alt="向上" >
        </button>
        <button class="scroll-button" @click="scrollToBottom">
            <img class="icon"  src="../assets/down.png" alt="向下" >
        </button>
      </div>
    </div>
  </template>
  

  
  <script>
  import '../assets/css/ArticleDetails.css';
  import Comment from '@/components/comment.vue'
  export default {
    name: 'ArticleDetails',
    data() {
      return {
        article: {},
        isFavorite: false,
        isLiked: false
      }
    },

    components: {
    Comment,
    },

    mounted() {
      this.article = this.$store.state.articledetail
    },
    methods: {
      goTo(path) {
      this.$router.push(path);
      },
      formatDate(dateStr) {
        const date = new Date(dateStr)
        const year = date.getFullYear()
        const month = date.getMonth() + 1
        const day = date.getDate()
        return `${year}-${month}-${day}`
      },
      toggleFavorite() {
        this.isFavorite = !this.isFavorite
      },
      toggleLike() {
       this.isLiked = !this.isLiked
      },
      scrollToTop() {
        window.scrollTo({ top: 0, behavior: 'smooth' })
      },
      scrollToBottom() {
        const scrollHeight = document.documentElement.scrollHeight
        window.scrollTo({ top: scrollHeight, behavior: 'smooth' })
      }
    }
  }
  </script>