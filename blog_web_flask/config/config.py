# config.py
import pymysql
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'db': 'qimo',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}