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
<<<<<<< HEAD
    return render_template('index.html')
    # try:
    #     payload = jwt.decode(receive_token, SECRET_KEY, algorithms=['HS256'])
    #     user_info = db.users.find_one({'id':payload['id']})
    #     return render_template('index.html')
    # except jwt.ExpiredSignatureError: # 예외처리 스타트
    #     return redirect(url_for('index', msg="로그인 시간 만료"))
    # except jwt.exceptions.DecodeError:
    #     return redirect(url_for('index', msg="로그인 정보 x"))
=======

    comment_list = db.dbuser_moviedata.aggregate([
        {'$group': {'_id': '$movie_title', 'count': {'$sum':1}, 'star_avg':{'$avg':'$user_star'}}}
        , {'$sort':{'count': -1}}
    ])
    comments = list(comment_list)

    #메인랭크는 영화순위 중 1~3위 정보를 클라이언트에 내려준다.
    mainrank_list = []
    #서브랭크는 영화순위 중 1~3위 정보를 클라이언트에 내려준다.
    subrank_list = []
    for i in range(len(comments)):
        movies = db.dbmoviedata.find_one({'movie_title':comments[i]['_id']}, {'_id':False})
        if i < 3:
            movies['movie_rank'] = i+1
            mainrank_list.append(movies)
        else:
            movies['movie_rank'] = i+1
            subrank_list.append(movies)

    return render_template('index.html', mainrank_list=mainrank_list, subrank_list=subrank_list)
    try:
        payload = jwt.decode(receive_token, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({'id':payload['id']})
        return render_template('index.html')
    except jwt.ExpiredSignatureError: # 예외처리 스타트
        return redirect(url_for('index', msg="로그인 시간 만료"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('index', msg="로그인 정보 x"))
>>>>>>> a536a9ab5f7dfbc87aede91197c8d5212593f142

@app.route('/login')
def login():
    return render_template('login.html')

<<<<<<< HEAD
@app.route('/mypage')
def mypage():
    return render_template('mypage.html')


@app.route("/boardGet", methods=["GET"])
def board_get():
    myboard = list(db.users.find({}, {'_id': False}))
    return jsonify({'myboard': myboard})

@app.route("/memberRead", methods=["GET"])
def member_read():
    memberread = list(db.teamtest.find({}, {'_id': False}))
    return jsonify({'memberread': memberread})


@app.route("/mypageInfo", methods=["POST"])
def web_mars_post():
    # memberId_receive = request.form['memberId_give']
    memberName_receive = request.form['memberName_give']
    memberPhone_receive = request.form['memberPhone_give']
    memberEmail_receive = request.form['memberEmail_give']

    doc = {
        'name': memberName_receive,
        'phone': memberPhone_receive,
        'email': memberEmail_receive,
    }
    db.teamtest.insert_one(doc)
    return jsonify({'msg': '수정 완료 !'})


=======
@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/mem_area')
def memup():
    return render_template('mem_area.html')
>>>>>>> a536a9ab5f7dfbc87aede91197c8d5212593f142

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



# [유저 정보 확인 API]
# 로그인된 유저만 call 할 수 있는 API입니다.
# 유효한 토큰을 줘야 올바른 결과를 얻어갈 수 있습니다.
# (그렇지 않으면 남의 장바구니라든가, 정보를 누구나 볼 수 있겠죠?)
@app.route('/api/nick', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    # try / catch 문?
    # try 아래를 실행했다가, 에러가 있으면 except 구분으로 가란 얘기입니다.

    try:
        # token을 시크릿키로 디코딩합니다.
        # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        # 여기에선 그 예로 닉네임을 보내주겠습니다.
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': userinfo['nick']})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)