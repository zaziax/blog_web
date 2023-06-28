<template>
  <div class="app">
    <Nav @loginbt="showLogin = true"></Nav>
    <Login @registerbt="showRegister = true,showLogin = false" v-if="showLogin" @tourist="showLogin = false" @logok="showLogin=false"></Login>
    <Register v-if="showRegister" @tourist="showRegister = false" @regok="showRegister=false,showLogin = true"></Register>
    <div class="content">
      <div class="left">
        <router-view></router-view>
      </div>
      <div class="right">
        <StatisticCard></StatisticCard>
      </div>
    </div>
  </div>

</template>

<style scoped>
body {
    font-family: Arial, sans-serif;
    background-color: #f5f5f5;
    color: #333;
    margin: 0;
    padding: 0;
  }
  
.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f8fafc;
}

.content {
  display: flex;
  flex-direction: row;
  margin: 0 auto;
  margin-top: 20px;
  flex: 1;
  width: 90%;
}

.left {
  width: 80%;
  /* height: 80vh; */
  padding: 20px;
}

.right {
  width: 20%;
  height: 80vh;
  padding: 20px;
  
  border-left: 1px solid #e5e5e5;
}
</style>


<script>
import Nav from '@/components/nav.vue'
import Login from '@/components/user/login.vue'
import Register from '@/components/user/register.vue'
import StatisticCard from '@/components/statistic.vue'

export default{
  name :'APP',

  data(){
    return{
      showLogin: false,
      showRegister: false
    }
  },

  methods: {
    },

  components:{
    Nav,
    Login,
    Register,
    StatisticCard

  },



}
</script>
