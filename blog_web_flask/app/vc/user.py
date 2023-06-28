from flask import jsonify, request, session 
from flask import Blueprint
from app.models.user import User
from auth import login_required

uservc = Blueprint('uservc',__name__)

##控制器部分================================================

##注册提交
@uservc.route('/api/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        user = User.find_by_username(username)
        if user:
            return jsonify({"message":"用户名重名!"})
        else:
            
            user = User(username, email, password)
           
            try:
                user.save()
            except Exception as e:
               return jsonify({"message":"邮箱已被注册！或其它异常！"})
            return jsonify({"message":"注册成功!"})


##登录提交
@uservc.route('/api/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user = User.find_by_username(username)
        if user is None or not user.check_password(password):
            return jsonify({"message":"用户名或密码错误"})
        else:
            session['username'] = username
            session['isadmin']  = user.is_admin
            session['userid']  = user.id
            print("是否是管理员",session['isadmin']) 
            # print(jsonify({"message":"登录成功！",'username':session.get('username')}))
            return jsonify({"message":"登录成功！",'username':session.get('username'),'userid':user.id})
            

##用户退出
@uservc.route('/api/logout', methods=['POST'])
@login_required
def logout():
    # session.pop('username', None)
    session.clear()
    # os.remove(os.path.join(app.config['SESSION_FILE_DIR'], session.sid))
    return jsonify({"message": "成功退出登录！"})
