<template>
<div class="overlay"></div>
<form class="register-form">
    <h2>注册</h2>
    <label  for="username"><b>用户名</b></label>
    <input type="text" placeholder="Enter username" name="username" v-model="username" required>
    
    <label for="email"><b>邮箱</b></label>
    <input type="email" placeholder="Enter Email" name="email" v-model="email" required>

    <label for="password"><b>密码</b></label>
    <input type="password" placeholder="Enter Password" name="password" v-model="password" required>

    <button @click.prevent="register" type="submit" class="btn">注册</button>
    <p @click="tourist" class="link">以游客身份继续</p>
  </form>

</template>

<script>

import '../../assets/css/login_registration.css'
import axios from 'axios' 
import {ElNotification} from 'element-plus'

export default {
  name: 'Register',

  data(){
    return {
      username:'',
      email:'',
      password:''
    }
  },

  methods:{
    // 当以游客身份继续被点击
    tourist(){
      this.$emit('tourist');
    },
    // 点击注册按钮
    register(){
      axios.post('/api/register', {
      username: this.username,
      email: this.email,
      password: this.password
      }).then(response => {
        if(response.data['message'] == '用户名重名!'){
          ElNotification({
              title: '注册不成功！',
              message: response.data['message'],
              type: 'warning',
              })
        }else if(response.data['message'] == '邮箱已被注册！或其它异常！'){
          ElNotification({
              title: '注册不成功！',
              message: response.data['message'],
              type: 'error',
              })
        }else{
          ElNotification({
              title: '注册成功！',
              message: '请登录！',
              type: 'success',
              })
          console.log(response.data);
          this.$emit("regok");
        }
          
        }).catch(error => {
          console.log(error.response.data);
        });
            }
  }
  
}
</script>