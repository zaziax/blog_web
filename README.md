# blog_web
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
