import pymysql.cursors
from config.config import DATABASE_CONFIG
import hashlib
import uuid

connection = pymysql.connect(**DATABASE_CONFIG)

class User(object):
    def __init__(self, username, email,password_hash,id=None,is_admin=None):
        if id is None:
            new_uuid = uuid.uuid4()
            uuid_str = str(new_uuid)
            self.id = uuid_str
        else:
            self.id = id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        if is_admin != None:
            self.is_admin = is_admin
        
    
    def save(self):
        password_hash = hashlib.md5(self.password_hash.encode('utf-8')).hexdigest()
        with connection.cursor() as cursor:
            sql = "INSERT INTO user (id, username, email, password_hash) VALUES (%s,%s, %s, %s)"
            cursor.execute(sql, (self.id, self.username, self.email, password_hash))
            connection.commit()

    @staticmethod
    def find_by_username(username):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM user WHERE username=%s"
            cursor.execute(sql, (username,))
            result = cursor.fetchone()
            if result:
                return User(result['username'], result['email'], result['password_hash'],result['id'],result['is_admin'])
            else:
                return None
    
    @staticmethod
    def find_by_id(id):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM user WHERE id=%s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            if result:
                return User(result['username'], result['email'], result['password_hash'],result['id'])
            else:
                return None

    def check_password(self, password):
        password_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
        return self.password_hash == password_hash


    #获取文章总数
    @staticmethod
    def count_all_users():
        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) FROM user"
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                return result['COUNT(*)']
            else:
                return 0



