from functools import wraps
from flask import jsonify, session, url_for, redirect

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'username' in session:
            return func(*args, **kwargs)
        else:
            return jsonify({"message":"请先登录!"})
    return wrapper