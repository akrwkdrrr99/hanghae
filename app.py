import jwt
import datetime

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.l91vj.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

SECRET_KEY = "MOVIEW"

@app.route('/')
def home():
    receive_token = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(receive_token, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({'id':payload['id']})
        return render_template('index.html')
    except jwt.ExpiredSignatureError: # 예외처리 스타트
        return redirect(url_for('index', msg="로그인 시간 만료"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('index', msg="로그인 정보 x"))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    receive_token = request.cookies.get('mytoken')
    print(receive_token)
    user_list = list(db.bucket.find({}, {'_id': False}))
#    session.pop('userid', None)
    session.clear()
    return redirect('/')


@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/memaree')
def memup():
    return render_template('memaree.html')

@app.route('/api', methods=["POST"])
def api():
    receive_reqtype = request.form['reqType']

    if receive_reqtype == 'getRequestLogin':
        receive_userid = request.form['userId']
        receive_userpw = request.form['userPw']
        result = db.users.find_one({'id': receive_userid, 'pw': receive_userpw})

        if result is not None:
            payload = {
                'id': receive_userid,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return jsonify({'code': 0, 'msg': '정상입니다.', 'token': token})

        else:
            return jsonify({'code': -1, 'msg': 'id/pw가 일치하지 않습니다.'})
    elif receive_reqtype == 'postRequestSignUp':
        receive_userid = request.form['userId']
        receive_userpw = request.form['userPw']
        receive_username = request.form['userName']
        receive_useremail = request.form['userEmail']
        receive_userphone = request.form['userPhone']
        doc = {
            'userid': receive_userid
            , 'userpw': receive_userpw
            , 'username': receive_username
            , 'useremail': receive_useremail
            , 'userphone': receive_userphone
        }
        db.users.insert_one(doc)
        return jsonify({'code': 0, 'msg': '회원가입 완료'})
    else:
        return jsonify({'code': -99, 'msg': '정의되지 않은 요청코드'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)