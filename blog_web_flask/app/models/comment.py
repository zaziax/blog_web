import pymysql.cursors
from app.models.article import Article
from app.models.user import User
from config.config import DATABASE_CONFIG
import uuid

connection = pymysql.connect(**DATABASE_CONFIG)

class Comment(object):
    def __init__(self, content, user_id, article_id,id=None,created_at =None):
        if id is None:
            new_uuid = uuid.uuid4()
            uuid_str = str(new_uuid)
            self.id = uuid_str
        else:
            self.id=id
        self.content = content
        self.user_id = user_id
        self.article_id = article_id
        self.created_at = created_at
    
    
    def save(self):
        with connection.cursor() as cursor:
            sql = "INSERT INTO Comment (id, content, user_id, article_id) VALUES (%s,%s, %s, %s)"
            cursor.execute(sql, (self.id, self.content, self.user_id, self.article_id))
            connection.commit()
    
    @staticmethod
    def find_by_id(comment_id):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Comment WHERE id=%s"
            cursor.execute(sql, (comment_id,))
            result = cursor.fetchone()
            if result:
                return Comment(result['content'], result['user_id'], result['created_id'])
            else:
                return None
    
    @staticmethod
    def find_by_article(article_id):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Comment WHERE article_id=%s"
            cursor.execute(sql, (article_id,))
            result = cursor.fetchall()
            if result:
                comments = []
                for row in result:
                    comment = Comment(row['content'], row['user_id'], row['article_id'],row['id'],row['created_at'])
                    comments.append(comment)
                return comments
            else:
                return None
    
    @staticmethod
    def find_by_article_by_page(limit,offset,article_id):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Comment WHERE article_id=%s ORDER BY created_at DESC LIMIT %s OFFSET %s"
            cursor.execute(sql, (article_id,limit,offset))
            result = cursor.fetchall()
            if result:
                comments = []
                for row in result:
                    comment = Comment(row['content'], row['user_id'], row['article_id'],row['id'],row['created_at'])
                    comments.append(comment)
                return comments
            else:
                return None
    
    def update(self):
        with connection.cursor() as cursor:
            sql = "UPDATE Comment SET content=%s, user_id=%s, article_id=%s WHERE id=%s"
            cursor.execute(sql, (self.content, self.user_id, self.article_id, self.id))
            connection.commit()
    
    def iddelete(id):
        with connection.cursor() as cursor:
            sql = "DELETE FROM Comment WHERE id=%s"
            cursor.execute(sql, (id,))
            connection.commit()

    def delete(article_id):
        with connection.cursor() as cursor:
            sql = "DELETE FROM Comment WHERE article_id=%s"
            cursor.execute(sql, (article_id,))
            connection.commit()
    
    def get_user(self):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM User WHERE id=%s"
            cursor.execute(sql, (self.user_id,))
            result = cursor.fetchone()
            if result:
                return User(result['username'], result['email'], result['password_hash'])
            else:
                return None
    
    def get_article(self):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Article WHERE id=%s"
            cursor.execute(sql, (self.article_id,))
            result = cursor.fetchone()
            if result:
                return Article(result['title'], result['content'], result['user_id'], result['category_id'])
            else:
                return None
            
    #获取评论总数
    @staticmethod
    def count_all_comment(search_query=None):
        with connection.cursor() as cursor:
            if search_query:
                sql ="SELECT COUNT(*) FROM Comment WHERE article_id = %s"
                cursor.execute(sql,(search_query,))
                result = cursor.fetchone()
                if result:
                    return result['COUNT(*)']
                else:
                    return 0

           
            
            
            