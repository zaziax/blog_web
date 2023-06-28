<template>
  <div class="about">
    <div class="author">
      <div class="author-avatar">
        <img src="http://sha.zazia.cn/upload/2021/12/psb%20(1)-9af77419601e414093520fba5cdf31a4.png" alt="zazia"/>
      </div>
      <div class="author-info">
        <div class="author-name">开发: zazia</div>
        <div class="author-email">邮箱：shaxiya@qq.com</div>
        <div class="author-email">网址：<a href="https://sha.zazia.cn/">sha.zazia.cn</a></div>
      </div>
    </div>
    <div class="tech-stack">
      <div class="tech-stack-item">
        <div class="tech-stack-label">前端</div>
        <div class="tech-stack-value">Vue3</div>
      </div>
      <div class="tech-stack-item">
        <div class="tech-stack-label">后端</div>
        <div class="tech-stack-value">Python</div>
      </div>
    </div>
    <div class="time">时间：2023年6月</div>
  </div>
</template>

<script>
  export default {
    name: 'About',
    data(){
        return{
            userCount:2,
            articleCount:12
        }
    }
  }
</script>

<style>
.about {
  max-width: 800px;
  margin: 0 auto;
  padding: 50px 20px;
}

.author {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 50px;
}

.author-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 20px;
}

.author-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.author-info {
  display: flex;
  flex-direction: column;
}

.author-name {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
}

.author-email {
  font-size: 16px;
  color: #666;
}

.tech-stack {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  margin-bottom: 50px;
}

.tech-stack-item {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin: 0 20px;
}

.tech-stack-label {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
}

.tech-stack-value {
  font-size: 16px;
  color: #666;
}

.time {
  text-align: center;
  font-size: 18px;
  color: #666;
}
</style>