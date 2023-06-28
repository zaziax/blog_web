import pymysql.cursors
from app.models.article import Article
from app.models.user import User
from config.config import DATABASE_CONFIG
import uuid

connection = pymysql.connect(**DATABASE_CONFIG)

class Like(object):
    def __init__(self, user_id, article_id):
        new_uuid = uuid.uuid4()
        uuid_str = str(new_uuid)
        self.id = uuid_str
        self.user_id = user_id
        self.article_id = article_id
    
    def save(self):
        with connection.cursor() as cursor:
            sql = "INSERT INTO Like (id, user_id, article_id) VALUES (%s,%s, %s)"
            cursor.execute(sql, (self.id, self.user_id, self.article_id))
            connection.commit()
    
    @staticmethod
    def find_by_id(like_id):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Like WHERE id=%s"
            cursor.execute(sql, (like_id,))
            result = cursor.fetchone()
            if result:
                return Like(result['user_id'], result['article_id'])
            else:
                return None
    
    @staticmethod
    def find_by_user(user_id):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Like WHERE user_id=%s"
            cursor.execute(sql, (user_id,))
            result = cursor.fetchall()
            if result:
                likes = []
                for row in result:
                    like = Like(row['user_id'], row['article_id'])
                    likes.append(like)
                return likes
            else:
                return None
    
    @staticmethod
    def find_by_article(article_id):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Like WHERE article_id=%s"
            cursor.execute(sql, (article_id,))
            result = cursor.fetchall()
            if result:
                likes = []
                for row in result:
                    like = Like(row['user_id'], row['article_id'])
                    likes.append(like)
                return likes
            else:
                return None
    
    def delete(self):
        with connection.cursor() as cursor:
            sql = "DELETE FROM Like WHERE id=%s"
            cursor.execute(sql, (self.id,))
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
    
    #获取文章点赞总数
    @staticmethod
    def count_all_like(search_query=None):
        with connection.cursor() as cursor:
            if search_query:
                sql ="SELECT COUNT(*) FROM articlelike WHERE article_id = %s"
                cursor.execute(sql,search_query)
                result = cursor.fetchone()
                if result:
                    return result['COUNT(*)']
                else:
                    return 0