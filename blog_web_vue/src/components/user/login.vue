<template>

<div class="overlay"></div>
<form class="login-form">
    <h2>登录</h2>
    <label for="username"><b>用户名</b></label>
    <input type="text" placeholder="Enter Username" name="username" v-model="username" required>

    <label for="password"><b>密码</b></label>
    <input type="password" placeholder="Enter Password" name="password" v-model="password" required>

    <button @click.prevent="login" type="submit" class="btn"><b>登录</b></button>
    没有账号？<p @click="registerbt" class="link">去注册！</p>
             <p @click="tourist" class="link">以游客身份继续</p>
  </form>

    
    </template>
    
    <script>
    import '../../assets/css/login_registration.css'
    import axios from 'axios' 
    import {ElNotification} from 'element-plus'

    export default {
      name: 'Login',

      data(){
    return {
      username:'',
      password:''
    }
  },

      methods:{
        // 去注册被点击
        registerbt(){
            this.$emit('registerbt');
        },
        //以游客身份继续被点击
        tourist(){
            this.$emit('tourist');
        },

            // 点击登录按钮
        login(){
        axios.post('/api/login', {
        username: this.username,
        password: this.password
        }).then(response => {
            console.log(response.data);
            if(response.data["message"] == "用户名或密码错误"){
              console.log(response.data["message"])
              ElNotification({
              title: '登录失败！',
              message: response.data["message"],
              type: 'error',
              })
            }else{
              // console.log(this.$store.state.isLoggedIn);
              this.$emit("logok");
              this.$store.dispatch('xlogin',{username:response.data['username'],userid:response.data['userid']}).then(() => {
              this.$emit('loggedIn')
              })
              console.log('ID:',this.$store.state.userid)
              console.log('用户名:',this.$store.state.username)
              //定时退出
              this.$store.dispatch('startLogoutTimer', 30 * 60 * 1000) 
              // console.log(this.$store.state.isLoggedIn);
              ElNotification({
              title: '登录成功！',
              message: '欢迎 ['+response.data['username']+'] !',
              type: 'success',
              })
            }
            
          }).catch(error => {
            console.log(error.response.data);
          });
              }
        }
      
    }
    </script>