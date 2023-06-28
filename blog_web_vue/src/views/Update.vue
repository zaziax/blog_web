<template>
    <div class="container">
      <div class="card">
        <div class="card-header">
          <h3>修改文章</h3>
          <button class="publish-btn" @click="publish">更新</button>
        </div>
        <div class="card-body">
          <div class="form-group">
            <label for="title">文章标题：</label>
            <input type="text" id="title" v-model="title" />
          </div>
          <div class="form-group">
            <label for="type">文章类型：</label>
            <select id="type" v-model="type">
              <option v-for="category in categorys" :key="category.id" :value="category.name">{{ category.name }}</option>
            </select>
          </div>
          <!-- <div class="form-group">
            <label for="image">文章封面：</label>
            <input type="file" id="image" @change="onImageChange" />
          </div>

          <div class="form-group">
            <label for="attachment">文章附件：</label>
            <input type="file" id="attachment" @change="onAttachmentChange" />
          </div> -->

          <div class="editor-wrapper">
            <div ref="editor"></div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Quill from 'quill';
  import "quill/dist/quill.core.css";
  import "quill/dist/quill.snow.css";
  import '../assets/css/Write.css';
  import axios from 'axios' 
  import {ElNotification} from 'element-plus'
  
  export default {
    name:'Update',
    data() {
      return {
        id:this.$store.state.articledetail.id,
        title: this.$store.state.articledetail.title,
        categorys:[],
        type: this.$store.state.articledetail.category_name,
        quill: null,
        imageUrl: '#',
        attachmentUrl: '#',
      }
    },
    mounted() {
      this.quill = new Quill(this.$refs.editor, {
        theme: 'snow'
      })

      // 将默认内容插入到 Quill 编辑器中
      const defaultContent = this.$store.state.articledetail.content;
      const delta = this.quill.clipboard.convert(defaultContent);
      this.quill.setContents(delta);
  
      axios.get('/api/getcategory')
      .then(response => {
      this.categorys = response.data.categorys;
      // 对返回的文章类别数据进行处理
      console.log(this.categorys);
      })
      .catch(error => {
      console.error(error);
      });

      console.log(this.$store.state.articledetail)
      

    },
    beforeUnmount() {
      this.quill = null

    },
    methods: {
      publish() {
        // 获取文章名称和选择的类型
        const articleName = this.title;
        const articleType = this.type;
  
        // 获取 Quill 编辑器中的内容
        const content = this.quill.root.innerHTML;
  
        // 将文章名称、选择的类型和 Quill 编辑器中的内容提交到后端
        axios.post('/api/articleupdate',{
            id:this.id,
            username:this.$store.state.username,
            title:articleName,
            articleType:articleType,
            content:content,
            imageUrl:this.imageUrl,
            attachmentUrl:this.attachmentUrl,
        }).then(response => {
            if(response.data['message'] == '文章发布成功!'){
                ElNotification({
              title: '更新成功！',
              message: '你更新了一篇新文章✨',
              type: 'success',
              })
            }

        }).catch(error =>{
            console.log(error.response.data);
        });
        console.log('发布文章');
        console.log(`文章名称：${articleName}`);
        console.log(`选择的类型：${articleType}`);
        console.log(`Quill 编辑器中的内容：${content}`);
      },

      onImageChange(event) {
        const file = event.target.files[0]; // 获取选中的图片文件
        if (!file) {
          return;
        }
        const formData = new FormData();
        formData.append('image', file);

        // 将图片上传到服务器
        axios
          .post('/api/upload-image', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          })
          .then((response) => {
            if (response.data.success) {
              ElNotification({
                title: '图片上传成功！',
                message: '文章图片已成功上传✨',
                type: 'success',
              });
              // 在此处保存图片的 URL 或其他信息，以便稍后将其与文章一起提交
              this.imageUrl = 'http://127.0.0.1:5000'+response.data.imageUrl;
              console.log('图片地址:',this.imageUrl);
            } else {
              ElNotification({
                title: '图片上传失败！',
                message: '请检查您的网络连接并重试',
                type: 'error',
              });
            }
          })
          .catch((error) => {
            console.error(error);
            ElNotification({
              title: '图片上传失败！',
              message: '请检查您的网络连接并重试',
              type: 'error',
            });
          });
      },


      onAttachmentChange(event) {
      const file = event.target.files[0]; // 获取选中的附件文件
      if (!file) {
        return;
      }
      const formData = new FormData();
      formData.append('attachment', file);

      // 将附件上传到服务器
      axios
        .post('/api/upload-attachment', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        .then((response) => {
          if (response.data.success) {
            ElNotification({
              title: '附件上传成功！',
              message: '文章附件已成功上传✨',
              type: 'success',
            });
            // 在此处保存附件的 URL 或其他信息，以便稍后将其与文章一起提交
            this.attachmentUrl = 'http://127.0.0.1:5000' + response.data.attachmentUrl;
            console.log('附件地址:', this.attachmentUrl);
          } else {
            ElNotification({
              title: '附件上传失败！',
              message: '请检查您的网络连接并重试',
              type: 'error',
            });
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },

      
    }
  }
  </script>
  
 
