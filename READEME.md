# 文章管理系统 #

## 一.系统要求 ##

### 1.用户角色 

1. **游客**：无需登录，可以查看所有文章和评论，但不能进行评论。
2. **注册用户** :需要登录，可以查看所有文章和评论，可以对文章进行评论，可以根据文章标题搜索文章。
3. **作者**:注册用户可以发布文章，可以管理自己的文章，可以针对自己文章的评论进行回复。
4. **管理员**:可以发布文章，可以管理所有的文章，可以针所有文章的评论进行回复，可以删除文章评论,注册用户管理。

### 2.功能



| 功能         | 要求                                                         | 完成状态🔴🟢 |
| ------------ | ------------------------------------------------------------ | ---------- |
| 多级页面     | 需要有至少三级页面                                           | 🟢          |
| 首页         | 显示文章分类与图片新闻等                                     | 🟢          |
| 二级页面     | 显示对应分类的文章                                           | 🟢          |
| 三级页面     | 显示文章具体内容                                             | 🟢          |
| 注册         | 首页提供注册**按钮** **页面** 验证手机号，<br />存储**MD5**加密的密码。 | 🟢          |
| 登录         | 与数据库对比信息，登录成功主页显示用户信息。                 | 🟢          |
| 导航栏       | 在任意页面均显示。                                           | 🟢          |
| 发布         | 1.文章分类发布<br /> 2.可以支持多个附件上传 <br />3.附件可下载 | 🟢🔴🟢        |
| 图片         | 上传一张图片作为新闻图片。                                   | 🟢          |
| 文章管理     | 1. 已经发布的文章，以列表方式显示。<br />2. 文章列表可根据标题进行搜索。<br />3. 文章列表可再次进行编辑、删除操作。<br />4.文章列表以分页方式显示。 | 🟢🟢         |
| 前台查看文章 | 1. 十条记录分页显示。<br />2. 文章搜索。<br />3. 三级页面显示文章详细内容。依据为文章id<br />4.实现文章生成二维码分享。 | 🟢🟢🟢🔴       |
| 评论         | 1. 以登录用户可以评论，也可以查看评论<br />2. 楼层功能（评论的评论） | 🟢🔴         |
| 联系方式     | --------------------------------                             |            |




### 3.数据库设计

1. **用户表**（User）

该表用于存储用户的基本信息，包括用户ID、用户名、密码、邮箱等。

```sql
CREATE TABLE User (
    id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    password_hash VARCHAR(128) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    is_admin BOOLEAN NOT NULL DEFAULT false
);
```

2. **文章表**（Article）

该表用于存储用户发布的文章信息，包括文章ID、标题、正文、发布时间、作者ID、分类ID等。

```sql
CREATE TABLE Article (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(256) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (category_id) REFERENCES Category(id)
);
```

3. **附件表**（Attachment）

该表用于存储用户上传的附件信息，包括附件ID、文件名、存储路径、上传时间、文章ID等。

```sql
CREATE TABLE Attachment (
    id VARCHAR(36) PRIMARY KEY,
    filename VARCHAR(256) NOT NULL,
    path VARCHAR(256) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    article_id INTEGER NOT NULL,
    FOREIGN KEY (article_id) REFERENCES Article(id)
);
```

4. **评论表**（Comment）

该表用于存储用户对文章的评论信息，包括评论ID、评论内容、评论时间、作者ID、文章ID等。

```sql
CREATE TABLE Comment (
    id VARCHAR(36) PRIMARY KEY,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    article_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (article_id) REFERENCES Article(id)
);
```

5. **点赞表**（Like）

该表用于存储用户对文章的点赞信息，包括点赞ID、点赞时间、作者ID、文章ID等。

```sql
CREATE TABLE Like (
    id VARCHAR(36) PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    article_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (article_id) REFERENCES Article(id)
);
```

6. **浏览统计表**（ViewCount）

该表用于存储用户对文章的浏览统计信息，包括文章ID、浏览次数等。

```sql
CREATE TABLE ViewCount (
    article_id INTEGER PRIMARY KEY,
    count INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (article_id) REFERENCES Article(id)
);
```

7. **文章分类表**（Category）

该表用于存储文章分类信息，包括分类ID、分类名称、分类描述、是否为管理员分类等。

```sql
CREATE TABLE Category (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(64) NOT NULL UNIQUE,
    description TEXT,
    is_admin BOOLEAN NOT NULL DEFAULT false
);
```

8. **收藏夹表**（Favorite）

该表用于存储用户创建的收藏夹信息，包括收藏夹ID、收藏夹名称、创建时间、作者ID等。

```sql
CREATE TABLE Favorite (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id)
);
```

9. **收藏夹文章表**（FavoriteArticle）

该表用于存储用户收藏的文章信息，包括收藏夹ID、文章ID等。

```sql
CREATE TABLE FavoriteArticle (
    favorite_id INTEGER NOT NULL,
    article_id INTEGER NOT NULL,
    PRIMARY KEY (favorite_id, article_id),
    FOREIGN KEY (favorite_id) REFERENCES Favorite(id),
    FOREIGN KEY (article_id) REFERENCES Article(id)
);
```



### 4.扩展功能 

> （打√为计划完成的内容）

* 作者关注及粉丝管理

* - [x] 文章收藏

* - [ ] 积分管理

* - [x] 点击率统计

### 5.UI    

![image-20230509195939379](C:\Users\zazia\AppData\Roaming\Typora\typora-user-images\image-20230509195939379.png)





### 6.开发顺序

```
开发一个文章管理系统需要考虑很多方面，包括用户认证、文章管理、文章分类、文章标签、文章评论等等。以下是一个较为完整的文章管理系统的功能开发顺序：

用户认证和授权：首先需要实现用户注册、登录、注销等基本的用户认证功能，并添加用户角色和权限控制，以确保只有授权用户才能进行文章管理操作。

文章管理：实现对文章的增、删、改、查等基本操作，并添加文章状态、发布时间、修改时间、作者等信息，以及文章封面图片、附件等其它元素。

文章分类和标签：实现对文章进行分类和标签，以方便用户查找和管理文章。可以考虑使用树形结构的分类、多级标签等方式。

文章评论：实现对文章进行评论、回复等操作，可以添加评论审核、敏感词过滤等功能，以确保评论内容的合法性和安全性。

搜索和过滤：实现文章的搜索、排序、过滤等功能，以方便用户查找和管理文章。

阅读统计和推荐：添加文章的阅读统计、点赞、收藏等功能，以及文章的推荐、热门排行等功能，提升用户体验和用户黏性。

SEO 优化和静态化：优化文章的标题、描述、关键词等元素，以提升文章在搜索引擎中的排名，同时实现文章的静态化，提升网站性能和用户体验。

数据备份和恢复：实现数据库的备份和恢复功能，以确保文章数据的安全性和可靠性。

以上是一个较为完整的文章管理系统的功能开发顺序，当然具体的开发流程还需要根据实际情况进行调整和补充。在开发过程中，需要注意代码的可维护性、可扩展性和安全性等方面，以确保系统的稳定性和可靠性。
```



## 二.问题记录表

### 1.vuex状态管理

在 Vue 3 中，你可以使用 Vuex 来管理应用程序的状态。Vuex 是一个专门为 Vue.js 应用程序开发的状态管理库。它通过一个全局的状态管理器来管理应用程序的状态，并提供了一些强大的工具来帮助你更好地组织和管理应用程序的数据。

要在 Vue 3 中使用 Vuex，你需要按照以下步骤进行操作：

1. 安装 Vuex：你可以通过命令 `npm install vuex` 或 `yarn add vuex` 来安装 Vuex。

2. 创建一个 Vuex Store：在你的 Vue 3 应用程序中，你需要创建一个 Vuex Store 来管理应用程序的状态。你可以在一个单独的 JavaScript 文件中创建 Vuex Store，例如 `store.js` 文件。

    在 `store.js` 文件中，你需要导入 Vuex 并创建一个新的 Vuex Store 对象。例如：

    ```javascript
    import { createStore } from 'vuex'

    const store = createStore({
      state() {
        return {
          username: null,
          isLoggedIn: false
        }
      },
      mutations: {
        setUsername(state, username) {
          state.username = username
        },
        setIsLoggedIn(state, isLoggedIn) {
          state.isLoggedIn = isLoggedIn
        }
      },
      actions: {
        login({ commit }, username) {
          // 在这里你可以向 Flask 服务器发送一个登录请求
          // 如果登录成功，将 username 和 isLoggedIn 设置为 true
          commit('setUsername', username)
          commit('setIsLoggedIn', true)
        },
        logout({ commit }) {
          // 在这里你可以向 Flask 服务器发送一个注销请求
          // 如果注销成功，将 username 和 isLoggedIn 设置为 null 和 false
          commit('setUsername', null)
          commit('setIsLoggedIn', false)
        }
      }
    })

    export default store
    ```

    在上面的代码中，我们定义了一个包含两个状态属性的 Vuex Store：`username` 和 `isLoggedIn`。我们还定义了两个 mutations：`setUsername` 和 `setIsLoggedIn`，以及两个 actions：`login` 和 `logout`。

3. 在 Vue 应用程序中使用 Vuex Store：在你的 Vue 3 应用程序中，你需要将创建的 Vuex Store 导入并添加到 Vue 应用程序中。例如：

    ```javascript
    import { createApp } from 'vue'
    import App from './App.vue'
    import store from './store'

    const app = createApp(App)
    app.use(store)
    app.mount('#app')
    ```

    在上面的代码中，我们将创建的 Vuex Store 添加到了我们的 Vue 应用程序中。现在，我们可以在 Vue 组件中使用 Vuex Store 中的状态和 mutations/actions 了。

4. 在 Vue 组件中使用 Vuex Store：在你的 Vue 组件中，你可以使用 Vuex Store 中的状态属性、mutations 和 actions。例如，在你的组件中，你可以使用以下代码来获取 `username` 状态属性：

    ```javascript
    import { mapState } from 'vuex'
    
    export default {
      computed: {
        ...mapState(['username'])
      }
    }
    ```

    在上面的代码中，我们使用了 `mapState` 辅助函数来获取 `username` 状态属性并将其映射到组件的计算属性中。

    如果你想要在组件中使用 mutations 或 actions，你可以使用 `commit` 或 `dispatch` 方法来触发它们。例如：

    ```javascript
    import { mapMutations, mapActions } from 'vuex'
    
    export default {
      methods: {
        ...mapMutations(['setUsername', 'setIsLoggedIn']),
        ...mapActions(['login', 'logout']),
        doLogin() {
          // 在这里你可以调用 login action 来登录用户
          this.login(this.username)
        }
      }
    }
    ```

    在上面的代码中，我们使用了 `mapMutations` 和 `mapActions` 辅助函数来获取 `setUsername`、`setIsLoggedIn`、`login` 和 `logout` mutations/actions，并将它们映射到组件的方法中。在 `doLogin` 方法中，我们调用了 `login` action 来登录用户。

综上所述，以上是使用 Vuex 在 Vue 3 中管理应用程序状态的基本步骤。你可以根据自己的需求和具体情况来调整 Vuex Store 的结构和 mutations/actions 的实现。对于保存来自 Flask 服务端的 session 信息，你可以在 Vuex Store 的状态属性中添加一个 `sessionId` 属性，并在登录时将它保存到状态中。例如：

```javascript
const store = createStore({
  state() {
    return {
      username: null,
      isLoggedIn: false,
      sessionId: null
    }
  },
  mutations: {
    setUsername(state, username) {
      state.username = username
    },
    setIsLoggedIn(state, isLoggedIn) {
      state.isLoggedIn = isLoggedIn
    },
    setSessionId(state, sessionId) {
      state.sessionId = sessionId
    }
  },
  actions: {
    async login({ commit }, { username, password }) {
      const response = await fetch('/api/login', {
        method: 'POST',
        body: JSON.stringify({ username, password })
      })
      const data = await response.json()
      if (data.success) {
        commit('setUsername', username)
        commit('setIsLoggedIn', true)
        commit('setSessionId', data.sessionId)
      }
    },
    async logout({ commit, state }) {
      const response = await fetch('/api/logout', {
        method: 'POST',
        body: JSON.stringify({ sessionId: state.sessionId })
      })
      const data = await response.json()
      if (data.success) {
        commit('setUsername', null)
        commit('setIsLoggedIn', false)
        commit('setSessionId', null)
      }
    }
  }
})
```

在上面的代码中，我们添加了一个 `sessionId` 状态属性，并在登录和注销时将其设置为来自 Flask 服务端的 session ID。在登录时，我们向 Flask 服务端发送一个登录请求，并在请求成功后将 `sessionId` 设置为返回的 session ID。在注销时，我们向 Flask 服务端发送一个注销请求，并在请求成功后将 `sessionId` 设置为 null。

你可以在组件中使用 `mapState` 辅助函数来获取 `sessionId` 状态属性。例如：

```javascript
import { mapState } from 'vuex'

export default {
  computed: {
    ...mapState(['sessionId'])
  }
}
```

这样，你就可以在组件中获取 `sessionId` 状态属性，并使用它来判断用户是否登录了。例如：

```javascript
<template>
  <div>
    <h1 v-if="isLoggedIn">Welcome, {{ username }}!</h1>
    <button v-if="isLoggedIn" @click="logout">Logout</button>
    <form v-else @submit.prevent="login">
      <label>Username:</label>
      <input v-model="username">
      <label>Password:</label>
      <input v-model="password" type="password">
      <button>Login</button>
    </form>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  computed: {
    ...mapState(['username', 'isLoggedIn'])
  },
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    ...mapActions(['login', 'logout'])
  },
  mounted() {
    if (this.isLoggedIn && !this.sessionId) {
      // 如果用户已登录但没有 sessionId，则向 Flask 服务端发送一个验证请求来获取 sessionId
      this.verifySession()
    }
  },
  async verifySession() {
    const response = await fetch('/api/verify_session', {
      method: 'POST',
      body: JSON.stringify({ username: this.username })
    })
    const data = await response.json()
    if (data.success) {
      this.$store.commit('setSessionId', data.sessionId)
    } else {
      this.$store.dispatch('logout')
    }
  }
}
</script>
```

在上面的代码中，我们在组件的 `mounted` 钩子函数中检查用户是否已登录，并且没有 `sessionId`。如果是这种情况，我们向 Flask 服务端发送一个验证请求来获取 `sessionId`，并将其保存到 Vuex Store 中。如果验证失败，则调用 `logout` action 注销用户。
