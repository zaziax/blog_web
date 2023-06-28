import pymysql.cursors
from app.models.article import Article
from config.config import DATABASE_CONFIG
import uuid

connection = pymysql.connect(**DATABASE_CONFIG)

class Attachment(object):
    def __init__(self, filename, path, article_id):
        new_uuid = uuid.uuid4()
        uuid_str = str(new_uuid)
        self.id = uuid_str
        self.filename = filename
        self.path = path
        self.article_id = article_id
    
    def save(self):
        with connection.cursor() as cursor:
            sql = "INSERT INTO Attachment (id, filename, path, article_id) VALUES (%s,%s, %s, %s)"
            cursor.execute(sql, (self.id, self.filename, self.path, self.article_id))
            connection.commit()
    
    @staticmethod
    def find_by_id(attachment_id):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Attachment WHERE id=%s"
            cursor.execute(sql, (attachment_id,))
            result = cursor.fetchone()
            if result:
                return Attachment(result['filename'], result['path'], result['article_id'])
            else:
                return None
    
    @staticmethod
    def find_by_article(article_id):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Attachment WHERE article_id=%s"
            cursor.execute(sql, (article_id,))
            result = cursor.fetchall()
            if result:
                attachments = []
                for row in result:
                    attachment = Attachment(row['filename'], row['path'], row['article_id'])
                    attachments.append(attachment)
                return attachments
            else:
                return None
    
    def update(self):
        with connection.cursor() as cursor:
            sql = "UPDATE Attachment SET filename=%s, path=%s, article_id=%s WHERE id=%s"
            cursor.execute(sql, (self.filename, self.path, self.article_id, self.id))
            connection.commit()
    
    def delete(article_id):
        with connection.cursor() as cursor:
            sql = "DELETE FROM Attachment WHERE article_id=%s"
            cursor.execute(sql, (article_id,))
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