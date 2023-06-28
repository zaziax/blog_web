<template>
    <div class="user-profile-page">

      <!-- 用户头像和名称 -->
      <div class="user-profile-header">
        <img :src="avatarUrl" alt="User Avatar">
        <h1>{{ this.$store.state.username }}</h1>
      </div>

      <nav class="user-profile-nav">
        <router-link to="/Write">撰  写</router-link>
        <!-- <router-link to="/messages">消  息</router-link> -->
        <router-link to="/Edit">管  理</router-link>
      </nav>

      <!-- 用户其他信息 -->
      <div class="user-profile-content">
        <!-- 这里可以添加用户的其他信息，例如文章列表、收藏夹等 -->
      </div>
      
      <!-- 退出登录按钮 -->
      <div class="user-profile-footer">
        <div class="user-profile-footer-b">
            <button @click="logout"></button>
        </div>
        
      </div>
    </div>
  </template>
  
  <script>
  import '../assets/css/user-profile.css';
  import axios from 'axios' 
  
  export default {
    name: 'PersonalPage',
  
    computed: {
      avatarUrl() {
        // 根据当前用户的信息生成头像 URL
        // 假设头像文件名为 username.png，存储在 /static/avatar 目录下
        return `http://127.0.0.1:5000/static/avatar/default.png`;
      }
    },
  
    methods:{
      logout() {
        axios.post('/api/logout').then(response => {
          // 清除本地的登录状态
          this.$store.dispatch('xloginout');
          // 跳转到首页
          this.$router.push('/');
          console.log(response.data);
        }).catch(error => {
          console.log(error);
        });
      }
    }
  }
  </script>