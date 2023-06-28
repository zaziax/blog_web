from flask import session
import pymysql.cursors
from config.config import DATABASE_CONFIG
import uuid

connection = pymysql.connect(**DATABASE_CONFIG)

class Article(object):
    def __init__(self, title, content, user_id, category_id,id=None,created_at=None,imageurl=None):
        if id is None:
            new_uuid = uuid.uuid4()
            uuid_str = str(new_uuid)
            self.id = uuid_str
        else:
            self.id = id
        self.title = title
        self.content = content
        self.user_id = user_id
        self.category_id = category_id
        self.created_at = created_at
        self.cover_url = imageurl

    def save(self):
        with connection.cursor() as cursor:
            sql = "INSERT INTO Article (id, title, content, user_id, category_id,cover_url) VALUES (%s,%s, %s, %s, %s,%s)"
            cursor.execute(sql, (self.id, self.title, self.content, self.user_id, self.category_id,self.cover_url))
            connection.commit()
        return self.id
    
    #查询所有文章
    @staticmethod
    def get_all_articles():
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Article"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            if result:
                articles = []
                for row in result:
                    article = Article(row['title'], row['content'], row['user_id'], row['category_id'], row['id'],row['created_at'])
                    articles.append(article)
                return articles
            else:
                return None
    
    #按照指定页码查询
    # @staticmethod
    # def get_articles_by_page(limit, offset):
    #     with connection.cursor() as cursor:
    #         sql = "SELECT * FROM Article ORDER BY created_at DESC LIMIT %s OFFSET %s"
    #         cursor.execute(sql, (limit, offset))
    #         result = cursor.fetchall()
    #         if result:
    #             articles = []
    #             for row in result:
    #                 article = Article(row['title'], row['content'], row['user_id'], row['category_id'], row['id'], row['created_at'])
    #                 articles.append(article)
    #             return articles
    #         else:
    #             return None
            
    @staticmethod
    def get_articles_by_page(limit, offset, search_query=None):
        with connection.cursor() as cursor:
            if search_query:
                sql = "SELECT * FROM Article WHERE title LIKE %s ORDER BY created_at DESC LIMIT %s OFFSET %s"
                cursor.execute(sql, ('%' + search_query + '%', limit, offset))
            else:
                sql = "SELECT * FROM Article ORDER BY created_at DESC LIMIT %s OFFSET %s"
                cursor.execute(sql, (limit, offset))

            result = cursor.fetchall()
            if result:
                articles = []
                for row in result:
                    article = Article(row['title'], row['content'], row['user_id'], row['category_id'], row['id'], row['created_at'],row['cover_url'])
                    articles.append(article)
                return articles
            else:
                return None

    @staticmethod
    def edit_articles_by_page(limit, offset, search_query=None):
        with connection.cursor() as cursor:
            if search_query:
                if session['isadmin'] == 1:
                    sql = "SELECT * FROM Article WHERE title LIKE %s ORDER BY created_at DESC LIMIT %s OFFSET %s"
                    cursor.execute(sql, ('%' + search_query + '%', limit, offset))
                else:
                    sql = "SELECT * FROM Article WHERE user_id=%s WHERE title LIKE %s ORDER BY created_at DESC LIMIT %s OFFSET %s"
                    cursor.execute(sql, (session['userid'],'%' + search_query + '%', limit, offset))

            else:
                if session['isadmin'] == 1:
                    sql = "SELECT * FROM Article ORDER BY created_at DESC LIMIT %s OFFSET %s"
                    cursor.execute(sql, (limit, offset))
                else:
                    sql = "SELECT * FROM Article WHERE user_id=%s ORDER BY created_at DESC LIMIT %s OFFSET %s"
                    cursor.execute(sql, (session['userid'],limit, offset))


            result = cursor.fetchall()
            if result:
                articles = []
                for row in result:
                    article = Article(row['title'], row['content'], row['user_id'], row['category_id'], row['id'], row['created_at'],row['cover_url'])
                    articles.append(article)
                return articles
            else:
                return None     
    
    #获取文章总数
    @staticmethod
    def ecount_all_articles(search_query=None):
        with connection.cursor() as cursor:
            if search_query:
                if session['isadmin'] == 1: 
                    sql ="SELECT COUNT(*) FROM Article WHERE title LIKE %s"
                    cursor.execute(sql,('%'+search_query+'%',))
                else:
                    sql ="SELECT COUNT(*) FROM Article WHERE user_id=%s WHERE title LIKE %s"
                    cursor.execute(sql,(session['userid'],'%'+search_query+'%',))
            else:
                if session['isadmin'] == 1: 
                    sql = "SELECT COUNT(*) FROM Article"
                    cursor.execute(sql)
                else:
                    sql = "SELECT COUNT(*) FROM Article WHERE user_id=%s"
                    cursor.execute(sql,(session['userid'],))

            result = cursor.fetchone()
            if result:
                return result['COUNT(*)']
            else:
                return 0
    
    #获取文章总数-管理
    @staticmethod
    def count_all_articles(search_query=None):
        with connection.cursor() as cursor:
            if search_query:
                sql ="SELECT COUNT(*) FROM Article WHERE title LIKE %s"
                cursor.execute(sql,('%'+search_query+'%',))
            else:
                sql = "SELECT COUNT(*) FROM Article"
                cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                return result['COUNT(*)']
            else:
                return 0
    
    #获取分类文章总数
    @staticmethod
    def count_all_articles_category(category_id=None):
        with connection.cursor() as cursor:
            if category_id:
                sql ="SELECT COUNT(*) FROM Article WHERE category_id= %s"
                cursor.execute(sql,(category_id,))
            result = cursor.fetchone()
            if result:
                return result['COUNT(*)']
            else:
                return 0
            
    
    @staticmethod
    def find_by_id(article_id):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Article WHERE id=%s"
            cursor.execute(sql, (article_id,))
            result = cursor.fetchone()
            if result:
                return Article(result['title'], result['content'], result['user_id'], result['category_id'])
            else:
                return None
    
    @staticmethod
    def find_by_category(limit,offset,category_id):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Article WHERE category_id=%s ORDER BY created_at DESC LIMIT %s OFFSET %s"
            cursor.execute(sql, (category_id,limit,offset))
            
            result = cursor.fetchall()
            if result:
                articles = []
                for row in result:
                    article = Article(row['title'], row['content'], row['user_id'], row['category_id'], row['id'], row['created_at'],row['cover_url'])
                    articles.append(article)
                return articles
            else:
                return None
    
    def update(self):
        with connection.cursor() as cursor:
            sql = "UPDATE Article SET title=%s, content=%s, user_id=%s, category_id=%s WHERE id=%s"
            cursor.execute(sql, (self.title, self.content, self.user_id, self.category_id, self.id))
            connection.commit()
    
    def delete(self):
        with connection.cursor() as cursor:
            sql = "DELETE FROM Article WHERE id=%s"
            cursor.execute(sql, (self.id,))
            connection.commit()
    
    def delete(article_id):
        with connection.cursor() as cursor:
            sql = "DELETE FROM Article WHERE id=%s"
            cursor.execute(sql, (article_id,))
            connection.commit()
    
    def get_user(self):
        from app.models.user import User
        with connection.cursor() as cursor:
            sql = "SELECT * FROM User WHERE id=%s"
            cursor.execute(sql, (self.user_id,))
            result = cursor.fetchone()
            if result:
                return User(result['username'], result['email'], result['password_hash'])
            else:
                return None
    
    def get_category(self):
        from app.models.category import Category
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Category WHERE id=%s"
            cursor.execute(sql, (self.category_id,))
            result = cursor.fetchone()
            if result:
                return Category(result['name'])
            else:
                return None