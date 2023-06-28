import pymysql.cursors

from config.config import DATABASE_CONFIG
import uuid

connection = pymysql.connect(**DATABASE_CONFIG)

class Category(object):
    def __init__(self, name, description=None, is_admin=False, id=None):
        if id is None:
            new_uuid = uuid.uuid4()
            uuid_str = str(new_uuid)
            self.id = uuid_str
        else:
            self.id = id
        self.name = name
        self.description = description
        self.is_admin = is_admin

    def save(self):
        with connection.cursor() as cursor:
            sql = "INSERT INTO Category (id, name, description, is_admin) VALUES (%s,%s, %s, %s)"
            cursor.execute(sql, (self.id, self.name, self.description, self.is_admin))
            connection.commit()
    
    @staticmethod
    def find_by_id(category_id):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Category WHERE id=%s"
            cursor.execute(sql, (category_id,))
            result = cursor.fetchone()
            if result:
                return Category(result['name'], result['description'], result['is_admin'])
            else:
                return None
    
    @staticmethod
    def find_by_name(name):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Category WHERE name=%s"
            cursor.execute(sql, (name,))
            result = cursor.fetchone()
            if result:
                return Category(result['name'], result['description'], result['is_admin'],result['id'])
            else:
                return None
    
    def update(self):
        with connection.cursor() as cursor:
            sql = "UPDATE Category SET name=%s, description=%s, is_admin=%s WHERE id=%s"
            cursor.execute(sql, (self.name, self.description, self.is_admin, self.id))
            connection.commit()
    
    def delete(self):
        with connection.cursor() as cursor:
            sql = "DELETE FROM Category WHERE id=%s"
            cursor.execute(sql, (self.id,))
            connection.commit()
    
    def get_articles(self):
        from app.models.article import Article
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Article WHERE category_id=%s"
            cursor.execute(sql, (self.id,))
            result = cursor.fetchall()
            if result:
                articles = []
                for row in result:
                    article = Article(row['title'], row['content'], row['user_id'], row['category_id'])
                    articles.append(article)
                return articles
            else:
                return None
    
    @staticmethod
    def get_category():
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Category"
            cursor.execute(sql,)
            result = cursor.fetchall()
            if result:
                categorys = []
                for row in result:
                    category = Category(row['name'], row['description'], row['is_admin'],row['id'])
                    categorys.append(category)
                return categorys
            else:
                return None