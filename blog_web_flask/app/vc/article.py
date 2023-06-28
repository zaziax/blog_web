from flask import Blueprint, Flask, jsonify, request, url_for
from app.models.article import Article
from werkzeug.utils import secure_filename
import os

articlevc = Blueprint('articlevc',__name__)

# 文章部分=====================================================================================================
# 发布文章
@articlevc.route('/api/articlesubmission', methods=['POST'])
def create_article():

    from app.models.category import Category
    from app.models.user import User
    from app.models.attachement import Attachment

    # 解析请求数据
    if request.method == 'POST':
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        imageurl = data.get('imageUrl')
        if imageurl == '#':
            imageurl = 'http://127.0.0.1:5000/static/articleimg/default.png'
        attachmentUrl = data.get('attachmentUrl')
        # user_id = request.form.get('user_id')
        user_id = User.find_by_username(data.get('username')).id
        # category_id = request.form.get('category_id')
        category_id = Category.find_by_name(data.get('articleType')).id
        # 创建文章对象
        article = Article(title=title, content=content, user_id=user_id, category_id=category_id,imageurl=imageurl)
        # 保存文章
        article_id = article.save()

        #文章是否有附件
        if attachmentUrl != '#': #执行保存附件
            filename = os.path.basename(attachmentUrl)
            attachment = Attachment(filename,attachmentUrl,article_id)
            attachment.save()
        return jsonify({"message":"文章发布成功!"})

# 更新文章
@articlevc.route('/api/articleupdate', methods=['POST'])
def update_article():

    from app.models.category import Category
    from app.models.user import User
    from app.models.attachement import Attachment

    # 解析请求数据
    if request.method == 'POST':
        data = request.get_json()
        id = data.get('id')
        title = data.get('title')
        content = data.get('content')

        print("修改的内容:",content)
        print("修改的id:",id)

        # user_id = request.form.get('user_id')
        user_id = User.find_by_username(data.get('username')).id
        # category_id = request.form.get('category_id')
        category_id = Category.find_by_name(data.get('articleType')).id
        # 创建文章对象
        article = Article(title=title, content=content, user_id=user_id, category_id=category_id,id=id)
        # 保存文章
        article.update()

        # #文章是否有附件
        # if attachmentUrl != '#': #执行保存附件
        #     filename = os.path.basename(attachmentUrl)
        #     attachment = Attachment(filename,attachmentUrl,article_id)
        #     attachment.save()


        # 返回成功响应
        # return 'Article created successfully'
        # print(title,content,user_id,category_id)
        return jsonify({"message":"文章发布成功!"})



@articlevc.route('/api/articles',methods=['GET'])
def get_articles():
    from app.models.user import User
    from app.models.category import Category
    articles = Article.get_all_articles()

    if articles:
        article_list = []
        for article in articles:
            article_list.append({
                'id': article.id, # 文章id
                'title': article.title, #文章标题
                'content': article.content, #文章内容
                'user_id': article.user_id, #作者id
                'username': User.find_by_id(article.user_id,).username, #作者名称
                'category_id': article.category_id, #文章分类id
                'category_name': Category.find_by_id(article.category_id).name, #分类名称
                'created_at':article.created_at, #文章发布时间
                
            })
        return jsonify(article_list)
    else:
        return jsonify([])

 # 文章分页查询  
@articlevc.route('/api/articles/page/<int:page>',methods=['GET'])
def get_articles_by_page(page=1,per_page=None):
    from app.models.user import User
    from app.models.category import Category
    from app.models.like import Like
    from app.models.comment import Comment
    
    if per_page is None:
        per_page = int(request.args.get('per_page'))
    # print("条数:",total)
    offset = (page - 1) * per_page
    limit = per_page

    # print('显示条数:',limit,'偏移量:',offset)
    searchtext = request.args.get('searchtext')
    # print('查询字段：',searchtext)
    if searchtext != '':
        total = Article.count_all_articles(searchtext)
        articles = Article.get_articles_by_page(limit, offset,searchtext)
    else:
        total = Article.count_all_articles()
        articles = Article.get_articles_by_page(limit, offset)
    # print(articles)
    if articles:
        article_list = []
        for article in articles:
            article_list.append({
                'id': article.id, # 文章id
                'title': article.title, #文章标题
                'content': article.content, #文章内容
                'user_id': article.user_id, #作者id
                'username': User.find_by_id(article.user_id,).username, #作者名称
                'category_id': article.category_id, #文章分类id
                'category_name': Category.find_by_id(article.category_id).name, #分类名称
                'created_at':article.created_at, #文章发布时间
                'count_all_comment':Comment.count_all_comment(article.id),#总评论数量
                'count_all_like':Like.count_all_like(article.id), #总点赞数量
                'imageurl':article.cover_url, #文章封面图
                
            })
        return jsonify({'total': total, 'articles': article_list})
    else:
        return jsonify({'total': 0, 'articles': []})
    
# 文章管理 
@articlevc.route('/api/articlesedit/page/<int:page>',methods=['GET'])
def edit_articles_by_page(page=1,per_page=None):
    from app.models.user import User
    from app.models.category import Category
    from app.models.like import Like
    from app.models.comment import Comment

    if per_page is None:
        per_page = int(request.args.get('per_page'))
    
    offset = (page - 1) * per_page
    limit = per_page
    # print('显示条数:',limit,'偏移量:',offset)
    searchtext = request.args.get('searchtext')
    # print('查询字段：',searchtext)
    if searchtext != '':
        total = Article.ecount_all_articles(searchtext)
        articles = Article.edit_articles_by_page(limit, offset,searchtext)
    else:
        total = Article.ecount_all_articles()
        articles = Article.edit_articles_by_page(limit, offset)
    # print(articles)
    if articles:
        article_list = []
        for article in articles:
            article_list.append({
                'id': article.id, # 文章id
                'title': article.title, #文章标题
                'content': article.content, #文章内容
                'user_id': article.user_id, #作者id
                'username': User.find_by_id(article.user_id,).username, #作者名称
                'category_id': article.category_id, #文章分类id
                'category_name': Category.find_by_id(article.category_id).name, #分类名称
                'created_at':article.created_at, #文章发布时间
                'count_all_comment':Comment.count_all_comment(article.id),#总评论数量
                'count_all_like':Like.count_all_like(article.id), #总点赞数量
                'imageurl':article.cover_url, #文章封面图
                
            })
        return jsonify({'total': total, 'articles': article_list})
    else:
        return jsonify({'total': 0, 'articles': []})

 # 分类查询文章  
@articlevc.route('/api/articles/getbycategory/<int:page>',methods=['GET'])
def get_articles_by_category(page=1,per_page=15):
    from app.models.user import User
    from app.models.category import Category
    from app.models.like import Like
    from app.models.comment import Comment

        # print("条数:",total)
    offset = (page - 1) * per_page
    limit = per_page
    
    category_id = request.args.get('category_id')

    if category_id:
        total = Article.count_all_articles_category(category_id)
        articles = Article.find_by_category(limit,offset,category_id)
    if articles:
        article_list = []
        for article in articles:
            article_list.append({
                'id': article.id, # 文章id
                'title': article.title, #文章标题
                'content': article.content, #文章内容
                'user_id': article.user_id, #作者id
                'username': User.find_by_id(article.user_id,).username, #作者名称
                'category_id': article.category_id, #文章分类id
                'category_name': Category.find_by_id(article.category_id).name, #分类名称
                'created_at':article.created_at, #文章发布时间
                'count_all_comment':Comment.count_all_comment(article.id),#总评论数量
                'count_all_like':Like.count_all_like(article.id), #总点赞数量
                'imageurl':article.cover_url, #文章封面图
                
            })
        return jsonify({'total': total, 'articles': article_list})
    else:
        return jsonify({'total': 0, 'articles': []})
    
#获取文章分类
@articlevc.route('/api/getcategory',methods=['GET'])
def getcategory():
    from app.models.category import Category
    categorys = Category.get_category()
    if categorys:
        category_list = []
        for category in categorys:
            category_list.append({
                'id':category.id, #类别id
                'name':category.name, #类别名称
                'description':category.description #类别描述
            })
        return jsonify({'categorys':category_list})
    else:
        return jsonify({'categorys':[]})
    
@articlevc.route('/api/comments/delete', methods=['POST'])
def delete_article():
    from app.models.comment import Comment
    # 从请求体中读取文章 ID
    id = request.json.get('id')
    #删除评论
    Comment.iddelete(id)
    # 返回一个成功的响应
    return jsonify({'message': '评论删除成功'})


@articlevc.route('/api/delete-article', methods=['POST'])
def delete_comments():
    from app.models.comment import Comment
    from app.models.attachement import Attachment
    # 从请求体中读取文章 ID
    article_id = request.json.get('articleId')
    #删除评论
    Comment.delete(article_id)
    #删除附件
    Attachment.delete(article_id)
    #删除文章自身
    Article.delete(article_id)

    # 返回一个成功的响应
    return jsonify({'message': '文章删除成功'})

#图片与附件部分==============================================================================
#图片上传
# 定义允许上传的图片类型
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 检查上传的文件是否是图片文件
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 处理上传图片的请求
@articlevc.route('/api/upload-image', methods=['POST'])
def upload_image():
    # 检查是否有上传的文件
    if 'image' not in request.files:
        return jsonify({'success': False, 'message': 'No image uploaded'}), 400
    
    # 获取上传的图片文件
    file = request.files['image']
    # 检查文件名称是否为空
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No image selected'}), 400
    
    # 检查文件类型是否为允许的类型
    if file and allowed_file(file.filename):
        # 生成安全的文件名
        filename = secure_filename(file.filename)
        # 将文件保存到指定的目录中
        file.save(os.path.join('static/articleimg/', filename))
        # 返回成功信息以及图片的 URL
        return jsonify({'success': True, 'message': 'Image uploaded', 'imageUrl': url_for('static', filename='articleimg/' + filename)}), 200
    else:
        # 返回错误信息
        return jsonify({'success': False, 'message': 'Invalid file type'}), 400
    
#附件上传
# 定义允许上传的附件类型
F_ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt','zip','exe'}

# 检查上传的文件是否是允许的附件类型
def f_allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in F_ALLOWED_EXTENSIONS

# 处理上传附件的请求
@articlevc.route('/api/upload-attachment', methods=['POST'])
def upload_attachment():
    # 检查是否有上传的文件
    if 'attachment' not in request.files:
        return jsonify({'success': False, 'message': 'No attachment uploaded'}), 400
    
    # 获取上传的附件文件
    file = request.files['attachment']
    # 检查文件名称是否为空
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No attachment selected'}), 400
    
    # 检查文件类型是否为允许的类型
    if file and f_allowed_file(file.filename):
        # 生成安全的文件名
        filename = secure_filename(file.filename)
        # 将文件保存到指定的目录中
        file.save(os.path.join('static/articleattachment/', filename))
        # 返回成功信息以及附件的 URL
        return jsonify({'success': True, 'message': 'Attachment uploaded', 'attachmentUrl': url_for('static', filename='articleattachment/' + filename)}), 200
    else:
        # 返回错误信息
        return jsonify({'success': False, 'message': 'Invalid file type'}), 400
    
@articlevc.route('/api/article/getattachments', methods=['POST'])
def get_attachments():
    from app.models.attachement import Attachment
    data = request.get_json()
    article_id = data.get('article_id')
    attachments = Attachment.find_by_article(article_id)
    if attachments:
        attachments_dict = [attachment.__dict__ for attachment in attachments]
        return jsonify({'success': True, 'attachments': attachments_dict}), 200
    else:
        return jsonify({'success': False, 'message': 'No attachments found'}), 404
#评论部分====================================================================================
#发布评论
@articlevc.route('/api/comments/submission', methods=['POST'])
def post_comment():
    from app.models.comment import Comment
    data = request.get_json()
    # print("打印:",data)
    if data:
        comment = Comment( data.get('content'), data.get('user_id'), data.get('article_id'))
        comment.save()
        return jsonify({'message': '发布成功!'})
    else:
        return jsonify({'message': '发布失败!'})
    


#获取评论
@articlevc.route('/api/comments/get', methods=['GET'])
def get_comments():
    from app.models.user import User
    from app.models.comment import Comment
    article_id = request.args.get('article_id')
    if article_id:
        comments = Comment.find_by_article(article_id)
        comments_list = []
        if comments:
            for comment in comments:
                comments_list.append({
                    'id':comment.id, #评论id
                    'user_id':comment.user_id, #评论者id
                    'username': User.find_by_id(comment.user_id).username, #作者名称
                    'article_id':comment.article_id, #评论文章id
                    'content':comment.content, #评论内容
                    'created_at':comment.created_at #评论发布时间
                })
            return jsonify(comments_list)
            
    return jsonify([])

#分页获取评论
@articlevc.route('/api/comments/get/<int:page>', methods=['GET'])
def get_comments_by_page(page=1, per_page=10):
    from app.models.user import User
    from app.models.comment import Comment

    offset = (page-1) * per_page
    limit = per_page
    article_id = request.args.get('article_id')
    # print("是否获取参数:",article_id)
    if article_id:
        total = Comment.count_all_comment(article_id)
        # comments = Comment.find_by_article(article_id)
        comments = Comment.find_by_article_by_page(limit,offset,article_id)
        comments_list = []
        if comments:
            for comment in comments:
                comments_list.append({
                    'id':comment.id, #评论id
                    'user_id':comment.user_id, #评论者id
                    'username': User.find_by_id(comment.user_id).username, #作者名称
                    'article_id':comment.article_id, #评论文章id
                    'content':comment.content, #评论内容
                    'created_at':comment.created_at #评论发布时间
                })
            return jsonify({'total':total,'comments':comments_list})
            
    return jsonify({'total':0,'comments':[]})
    
