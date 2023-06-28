from flask import Blueprint, jsonify, request
from app.models.article import Article
from app.models.user import User


statisticvc = Blueprint('statisticvc ',__name__)

# 获取站点信息
@statisticvc .route('/api/getstatistic', methods=['GET'])
def getstatistic():
    count_users = User.count_all_users()
    count_articles = Article.count_all_articles()
    return jsonify({'count_users':count_users,'count_articles':count_articles})

# AI 交流
