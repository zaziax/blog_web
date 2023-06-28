import pymysql.cursors
from app.models.user import User
from config.config import DATABASE_CONFIG
import uuid

connection = pymysql.connect(**DATABASE_CONFIG)

class Favorite(object):
    def __init__(self, name, user_id):
        new_uuid = uuid.uuid4()
        uuid_str = str(new_uuid)
        self.id = uuid_str
        self.name = name
        self.user_id = user_id
     
    def save(self):
        with connection.cursor() as cursor:
            sql = "INSERT INTO Favorite (id, name, user_id) VALUES (%s,%s, %s)"
            cursor.execute(sql, (self.id, self.name, self.user_id))
            connection.commit()
    
    @staticmethod
    def find_by_id(favorite_id):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Favorite WHERE id=%s"
            cursor.execute(sql, (favorite_id,))
            result = cursor.fetchone()
            if result:
                return Favorite(result['name'], result['user_id'])
            else:
                return None
    
    @staticmethod
    def find_by_user(user_id):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Favorite WHERE user_id=%s"
            cursor.execute(sql, (user_id,))
            result = cursor.fetchall()
            if result:
                favorites = []
                for row in result:
                    favorite = Favorite(row['name'], row['user_id'])
                    favorites.append(favorite)
                return favorites
            else:
                return None
    
    def update(self):
        with connection.cursor() as cursor:
            sql = "UPDATE Favorite SET name=%s, user_id=%s WHERE id=%s"
            cursor.execute(sql, (self.name, self.user_id, self.id))
            connection.commit()
    
    def delete(self):
        with connection.cursor() as cursor:
            sql = "DELETE FROM Favorite WHERE id=%s"
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