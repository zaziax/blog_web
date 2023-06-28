import pymysql.cursors
from app.models.article import Article
from config.config import DATABASE_CONFIG

connection = pymysql.connect(**DATABASE_CONFIG)

class ViewCount(object):
    def __init__(self, article_id, count=0):
        self.article_id = article_id
        self.count = count
    
    
    def save(self):
        with connection.cursor() as cursor:
            sql = "INSERT INTO ViewCount (article_id, count) VALUES (%s, %s) ON DUPLICATE KEY UPDATE count=count+1"
            cursor.execute(sql, (self.article_id, self.count))
            connection.commit()
    
    @staticmethod
    def find_by_article(article_id):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM ViewCount WHERE article_id=%s"
            cursor.execute(sql, (article_id,))
            result = cursor.fetchone()
            if result:
                return ViewCount(result['article_id'], result['count'])
            else:
                return None
    
    def update(self):
        with connection.cursor() as cursor:
            sql = "UPDATE ViewCount SET count=%s WHERE article_id=%s"
            cursor.execute(sql, (self.count, self.article_id))
            connection.commit()
    
    def delete(self):
        with connection.cursor() as cursor:
            sql = "DELETE FROM ViewCount WHERE article_id=%s"
            cursor.execute(sql, (self.article_id,))
            connection.commit()
    
    def get_article(self):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Article WHERE id=%s"
            cursor.execute(sql, (self.article_id,))
            result = cursor.fetchone()
            if result:
                return Article(result['title'], result['content'], result['user_id'], result['category_id'])
            else:
                return None