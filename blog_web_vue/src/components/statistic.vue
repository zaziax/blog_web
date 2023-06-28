<template>
    <div class="scard">
      <div class="scard-body">
        <div class="statistic">
          <div class="statistic-item">
            <div class="statistic-value">{{ userCount }}</div>
            <div class="statistic-label"><b>用户数量</b></div>
          </div>
          <div class="statistic-item">
            <div class="statistic-value">{{ articleCount }}</div>
            <div class="statistic-label"><b>文章总数</b></div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
import '../assets/css/statistic.css';
  export default {
    name: 'StatisticCard',
    data(){
        return{
            userCount:0,
            articleCount:0
        }
    },

    created() {
      axios.get('/api/getstatistic').then(response=>{
        this.userCount =  response.data['count_users'],
        this.articleCount = response.data['count_articles']
      }).catch(console.error());
    },
  }
  </script>
