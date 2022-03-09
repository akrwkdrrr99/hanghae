from pymongo import MongoClient
import jwt
import datetime

from bs4 import BeautifulSoup
import requests

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
app = Flask(__name__)

#승균님 데이터 베이스 연결
client = MongoClient('mongodb+srv://test:sparta@cluster0.l91vj.mongodb.net/Cluster0?retryWrites=true&w=majority')

db = client.dbsparta



SECRET_KEY = "MOVIEW"

@app.route('/')
def home():
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
    # return render_template('index.html', mainrank_list=mainrank_list, subrank_list=subrank_list)

    try:
        receive_token = request.cookies.get('mytoken')
        payload = jwt.decode(receive_token, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({'userid':payload['id']})
        if user_info is not None:
            return render_template('index.html', mainrank_list=mainrank_list, subrank_list=subrank_list, user_info=user_info)
        else:
            return redirect(url_for('login', msg="유저정보없음"))
    except jwt.ExpiredSignatureError: # 예외처리 스타트
        return redirect(url_for('login', msg="로그인 시간 만료"))
    except jwt.exceptions.DecodeError:
        return render_template('index.html', mainrank_list=mainrank_list, subrank_list=subrank_list)


@app.route('/login')
def login():
    return render_template('login.html')

@app.route("/useridchk", methods=["GET"])
def user_id_get():
    users_list = list(db.users.find({}, {'_id': False}))
    return jsonify({'users': users_list})


# @app.route("/login/pwfind", methods=["GET"])
# def login_pw_find():
#     user_list = list(db.users.find({}, {'_id': False}))
#     return jsonify({'users': user_list})
#
# @app.route("/login/idfind", methods=["GET"])
# def login_id_find():
#     user_list2 = list(db.users.find({}, {'_id': False}))
#     return jsonify({'users': user_list})

@app.route('/mypage')
def mypage():
    return render_template('mypage.html')


    #영화 데이터베이스 클라이언트로 내려주기
@app.route("/boardGet", methods=["GET"])
def board_get():
    myboard = list(db.dbmoviedata.find({}, {'_id': False}))
    return jsonify({'myboard': myboard})

    #회원 정보 데이터베이스 클라이언트로 내려주기
@app.route("/memberRead", methods=["GET"])
def member_read():
    memberread = list(db.users.find({}, {'_id': False}))
    return jsonify({'memberread': memberread})

    # 개인정보 수정을 위한 로그인한 본인의 정보 데이터베이스 확인 및 수정
@app.route("/mypageInfo", methods=["POST"])
def user_update():
    # token_receive = request.cookies.get('mytoken')
    #
    # # try / catch 문?
    # # try 아래를 실행했다가, 에러가 있으면 except 구분으로 가란 얘기입니다.
    #
    # try:
    #     # token을 시크릿키로 디코딩합니다.
    #     # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
    #     payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    #     print(payload)
    #
    #     # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
    #     # 여기에선 그 예로 닉네임을 보내주겠습니다.
    #     userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
    #     return jsonify({'result': 'success', 'nickname': userinfo['nick']})
    # except jwt.ExpiredSignatureError:
    #     # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
    #     return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    # except jwt.exceptions.DecodeError:
    #     return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})

    # 개인정보 수정 요청온 값.
    # memberId_receive = request.form['memberId_give']
    memberName_receive = request.form['memberName_give']
    memberPhone_receive = request.form['memberPhone_give']
    memberEmail_receive = request.form['memberEmail_give']

    # 내 개인정보 찾아서 수정하기
    db.users.update_one({'name': ''}, {'$set': {'username': memberName_receive}})
    db.users.update_one({'name': ''}, {'$set': {'userphone': memberPhone_receive}})
    db.users.update_one({'name': ''}, {'$set': {'useremail': memberEmail_receive}})

    return jsonify({'msg': '수정 완료 !'})


@app.route("/userDelete", methods=["POST"])
def user_delete():
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

    return jsonify({'msg': '회원탈퇴 되었습니다. 감사합니다.'})

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/memaree')
def memup():
    return render_template('memaree.html')

@app.route('/board')
def board():
    all_movies = list(db.dbmoviedata.find({}, {'_id': False}))
    return render_template('board.html', all_movies = all_movies)

@app.route('/board/<condition>/<serch_text>/<flag>')
def board_serch(condition, serch_text, flag):
    if(flag == "0") :
        return jsonify({'result': 'success', 'msg': '기다려주세요'})
    elif(flag == "1"):
        if(condition == "1") :
            serch_condition = "movie_title"
        elif(condition == "2") :
            serch_condition = "movie_director"
        elif(condition == "3") :
            serch_condition = "movie_actor"
        else :
            return redirect(url_for('board'))

        # serch_movies = list(db.dbmoviedata.find({"{0}".format(serch_condition) : serch_text}, {'_id': False}))
        serch_movies = list(db.dbmoviedata.find({}, {'_id': False}))
        serched_movies = []
        check_actors = []
        for serch_movie in serch_movies :
            if(condition != "3"):
                if( serch_text in serch_movie[serch_condition] ) :
                    serched_movies.append(serch_movie)
            else:
                actors = serch_movie[serch_condition]
                for actor in actors :
                    if( serch_text in actor ) :
                        check_actors.append(serch_movie)
                for check_actor in check_actors :
                    if(check_actor not in serched_movies):
                        serched_movies.append(serch_movie)

        return render_template('board.html', all_movies = serched_movies)

@app.route('/board_write')
def board_write():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        userinfo = db.users.find_one({'userid': payload['id']}, {'_id': 0})
        return render_template('board_write.html')
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return redirect(url_for('home'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('home'))

@app.route('/board_detail/<keyword>')
def board_detail(keyword):
    moviedata = list(db.dbmoviedata.find({'movie_arrindex': int(keyword)}, {'_id': False}))[0] #get영화 정보
    userdatas = list(db.dbuser_moviedata.find({'movie_title': moviedata['movie_title']}, {'_id': False})) #get유저 정보
    all_movies = list(db.dbmoviedata.find({}, {'_id': False}))
    #글 번호
    total_movie = len(all_movies)
    if(moviedata['movie_arrindex'] > 1) :
        pre_post = moviedata['movie_arrindex'] - 1
    elif(moviedata['movie_arrindex'] == 1) :
        pre_post = -1

    if(moviedata['movie_arrindex'] < total_movie) :
        next_post = moviedata['movie_arrindex'] + 1
    elif(moviedata['movie_arrindex'] == total_movie) :
        next_post = -2

    return render_template('board_detail.html', movie_title=moviedata['movie_title'], movie_director=moviedata['movie_director'],
                           movie_opendate=moviedata['movie_opendate'],
                           movie_avg_star=moviedata['movie_avg_star'],
                           movie_recommand=moviedata['movie_recommand'],
                           movie_image = moviedata['movie_image'],
                           movie_desc = moviedata['movie_desc'],
                           movie_actor = moviedata['movie_actor'],
                           pre_post  = pre_post,
                           next_post = next_post,
                           userdatas = userdatas
                           )

@app.route('/api', methods=["POST"])
def api():
    receive_reqtype = request.form['reqType']

    if receive_reqtype == 'getRequestLogin':
        receive_userid = request.form['userId']
        receive_userpw = request.form['userPw']
        result = db.users.find_one({'userid': receive_userid, 'userpw': receive_userpw})

        if result is not None:
            payload = {
                'id': receive_userid,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60*60*24)
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
    elif receive_reqtype == 'postMovieData':
        url_receive = request.form['url_give']

        #검색을 하면 dictionary 형태로 제공된다.
        result = db.dbmoviedata.find_one({'movie_url': url_receive})

        user_ID = request.form['user_ID_give']
        star_receive = request.form['star_give']
        comment_receive = request.form['comment_give']
        actor_arr_x = []
        
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        data = requests.get(url_receive, headers=headers)

        soup = BeautifulSoup(data.text, 'html.parser')

        title = soup.select_one('meta[property="og:title"]')['content']

        user_moviedata = {
            'movie_title': title,
            'user_ID' : user_ID,
            'user_star' : int(star_receive),
            'user_comment': comment_receive,
        }
        print(user_moviedata)
        db.dbuser_moviedata.insert_one(user_moviedata)

        
        if result is not None: # 이미 영화 데이터가 존재
            totalsum = 0
            avg_star = 0
            #기존 DB 검색
            all_user_moviedata = list(db.dbuser_moviedata.find({'movie_title': title}, {'_id': False}))
            #추천 수 변경
            pre_recommand = len(all_user_moviedata)
            cur_recommand = pre_recommand + 1
            #평균 별점 변경
            for user_moviedata in all_user_moviedata :
                totalsum += user_moviedata['user_star']
            avg_star = (totalsum + int(star_receive)) / cur_recommand  # 기존 데이터들의 별점 합 에다가 현재 추가 하려는 데이터의 별점 추가 후 나누기
            db.dbmoviedata.update_one({'movie_title': title}, {'$set': {'movie_recommand': cur_recommand}})
            db.dbmoviedata.update_one({'movie_title': title}, {'$set': {'movie_avg_star': avg_star}})
            return jsonify({'code': 10, 'msg': '이미 존재합니다.'})
        
        elif result is None: # 영화 데이터 X
            #먼저 영화 전체 데이터 읽어옴
            all_movies = list(db.dbmoviedata.find({}, {'_id': False}))
            #글 번호
            total_movie = len(all_movies)
            movie_arrindex = total_movie + 1
            #추천 수
            recommand = 1 #첫 등록이므로 추천 수는 무조건 1
            #평균 별점
            avg_star = int(star_receive) #첫 등록이므로 평균 별점은 무조건 현재 별점
            #영화 정보 크롤링
            image = soup.select_one('meta[property="og:image"]')['content']
            desc = soup.select_one('meta[property="og:description"]')['content']
            releaseDates = soup.select(
                'div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(4) > a')
            openYear = releaseDates[0].text
            openMonthDay = releaseDates[1].text
            releaseDate = openYear + openMonthDay

            actors = soup.select(
                'div.article > div.section_group.section_group_frst > div:nth-child(2) > div > ul')
            arr_actor_x = actors[0].text.strip().replace("감독", "").replace("주연", "").replace("조연", "").split("\n")
            for actor_o in arr_actor_x:
                if (actor_o != ""):
                    if (" 역" not in actor_o):
                        actor_arr_x.append(actor_o)
            movie_director = actor_arr_x[0]
            actor_arr_o = actor_arr_x[1:len(arr_actor_x)]

            moviedata = {
                'movie_title': title,
                'movie_image': image,
                'movie_desc': desc,
                'movie_opendate' : releaseDate.strip(),
                'movie_director' : movie_director,
                'movie_actor' : actor_arr_o,
                'movie_url' : url_receive,
                'movie_arrindex' : movie_arrindex,
                'movie_recommand' : recommand,
                'movie_avg_star' : avg_star
            }
            db.dbmoviedata.insert_one(moviedata)

            return jsonify({'code': 10, 'msg': '등록이 완료되었습니다.'})

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
