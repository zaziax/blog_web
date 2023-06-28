from flask import Flask, jsonify,request,session
from flask_session import Session
from flask_cors import CORS
from app.vc import uservc
from app.vc import articlevc
from app.vc import statisticvc

app = Flask(__name__)
app.config['SECRET_KEY'] = 'web2023-20221159117-nafwjrgawurfgwtufas'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

#处理跨域请求
CORS(app,supports_credentials=True, resources={r"/api/*": {"origins": "http://127.0.0.1:8080"}})


# 处理用户相关的控制
app.register_blueprint(uservc) 

#处理文章相关的控制
app.register_blueprint(articlevc)

#处理数据展示组件相关的控制
app.register_blueprint(statisticvc)


if __name__=='__main__':
    app.debug = True
    app.run()