import jwt
import datetime

from flask import Flask, render_template, request, jsonify, redirect, url_for
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.l91vj.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

SECRET_KEY = "MOVIEW"

@app.route('/')
def home():
    receive_token = request.cookies.get('mytoken')
    # return render_template('index.html')
    return render_template('board.html')
    # try:
    #     payload = jwt.decode(receive_token, SECRET_KEY, algorithms=['HS256'])
    #     user_info = db.users.find_one({'id':payload['id']})
    #     return render_template('index.html')
    # except jwt.ExpiredSignatureError: # 예외처리 스타트
    #     return redirect(url_for('index', msg="로그인 시간 만료"))
    # except jwt.exceptions.DecodeError:
    #     return redirect(url_for('index', msg="로그인 정보 x"))

@app.route('/login')
def login():
    return render_template('login.html')

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
    else:
        return jsonify({'code': -99, 'msg': '정의되지 않은 요청코드입니다.'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)