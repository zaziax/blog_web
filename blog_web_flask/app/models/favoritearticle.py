import pymysql.cursors
from app.models.article import Article
from app.models.favorite import Favorite
from config.config import DATABASE_CONFIG

connection = pymysql.connect(**DATABASE_CONFIG)

class FavoriteArticle(object):
    def __init__(self, favorite_id, article_id):
        self.favorite_id = favorite_id
        self.article_id = article_id
    
    def save(self):
        with connection.cursor() as cursor:
            sql = "INSERT INTO FavoriteArticle (favorite_id, article_id) VALUES (%s, %s)"
            cursor.execute(sql, (self.favorite_id, self.article_id))
            connection.commit()
    
    @staticmethod
    def find_by_favorite(favorite_id):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM FavoriteArticle WHERE favorite_id=%s"
            cursor.execute(sql, (favorite_id,))
            result = cursor.fetchall()
            if result:
                favorite_articles = []
                for row in result:
                    favorite_article = FavoriteArticle(row['favorite_id'], row['article_id'])
                    favorite_articles.append(favorite_article)
                return favorite_articles
            else:
                return None
    
    @staticmethod
    def find_by_article(article_id):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM FavoriteArticle WHERE article_id=%s"
            cursor.execute(sql, (article_id,))
            result = cursor.fetchall()
            if result:
                favorite_articles = []
                for row in result:
                    favorite_article = FavoriteArticle(row['favorite_id'], row['article_id'])
                    favorite_articles.append(favorite_article)
                return favorite_articles
            else:
                return None
    
    def delete(self):
        with connection.cursor() as cursor:
            sql = "DELETE FROM FavoriteArticle WHERE favorite_id=%s AND article_id=%s"
            cursor.execute(sql, (self.favorite_id, self.article_id))
            connection.commit()
    
    def get_favorite(self):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Favorite WHERE id=%s"
            cursor.execute(sql, (self.favorite_id,))
            result = cursor.fetchone()
            if result:
                return Favorite(result['name'], result['user_id'])
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