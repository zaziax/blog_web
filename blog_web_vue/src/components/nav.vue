<template>
  <div class="navbar">
    <div class="logo">SHA-web</div>
    <div class="links">
      <router-link to="/"><a href="#">主页</a></router-link>
      <router-link to="/Filing"><a href="#">分类</a></router-link>
      <!-- <router-link to="/"><a href="#">收藏夹</a></router-link> -->
      <router-link to="/about"><a href="#">关于</a></router-link>
    </div>
    <div v-if="this.$store.state.isLoggedIn == false" @click="loginbt" class="login">
      <a href="#">登录/注册</a>
    </div>
    <div @click="goTo('/PersonalPage')" v-else class="user-profile">
      <img src="http://127.0.0.1:5000/static/avatar/default.png" alt="User Avatar">
      <span>{{this.$store.state.username}}</span>
    </div>
  </div>
</template>

<script>
 import '../assets/css/nav.css';
 export default {
  name: 'Nav',

  data(){
    return{
      
    }
  },
  created() {
    // 监听 username 状态属性的变化
    this.$store.watch(
      (state) => state.username,
      // (newVal, oldVal) => {
      //   console.log('username changed:', newVal, oldVal)
      // }
      // this.username = this.$store.state.username,
    )
  },

  methods:{
    loginbt(){
      this.$emit('loginbt');
    },
    goTo(path){
      this.$router.push({ path });
    }

    
  }
  
}

</script>



