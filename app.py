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

    # DB에서 영화를 기준으로 집계하여 각 영화별 UserComment 수와 평균별점을 조회.
    comment_list = db.dbuser_moviedata.aggregate([
        {'$group': {'_id': '$movie_title', 'count': {'$sum': 1}, 'star_avg': {'$avg': '$user_star'}}}
        , {'$sort': {'count': -1, 'star_avg': -1, 'open_date': 1}}
    ])
    comments = list(comment_list)

    # # 각 (영화별 코멘트 수 / 전체 영화 코멘트 수) * 100 하여 백분율로 점수생성 후 총 점수 계산하여 리스트생성
    # arr_moviesranks = []
    # for comment in comments:
    #
    #     comment_percentage = int(comment['count'])/int(total_comment_cnt) * 100
    #     comment['comment_percentage'] = comment_percentage
    #     comment['movie_rank_point'] = comment_percentage + comment['star_avg']
    #     arr_moviesranks.append(comment)
    #
    # arr_sort_movierank = sorted(arr_moviesranks, key=lambda rank:(rank['movie_rank_point']), reverse=True)

    #메인랭크는 영화순위 중 1~3위 정보를 클라이언트에 내려준다.
    mainrank_list = []
    #서브랭크는 영화순위 중 1~3위 정보를 클라이언트에 내려준다.
    subrank_list = []
    for i in range(0, 10):

        movies = db.dbmoviedata.find_one({'movie_title':comments[i]['_id']}, {'_id':False})
        if i < 3:
            movies['movie_rank'] = i+1
            mainrank_list.append(movies)
        else:
            movies['movie_rank'] = i+1
            subrank_list.append(movies)

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

@app.route("/login/idfind", methods=["POST"])
def login_id_find():
    l_i_find_data1 = request.form['userName']
    l_i_find_data2 = request.form['userEmail']
    same_names = list(db.users.find({'username':l_i_find_data1}, {'_id': False}))

    if (len(same_names) < 1):
        return jsonify({'msg': '등록된 이름이 없습니다.'})
    elif (len(same_names) > 1):
        for user_s_list in same_names:
            if(user_s_list['useremail'] == l_i_find_data2):
                msg = "아이디는 다음과 같습니다." + user_s_list['userid']
            else:
                msg = "등록된 이메일이 아닙니다."
        return jsonify({'msg':  msg})
    else:
        return jsonify({'msg': "아이디는 다음과 같습니다." + same_names[0]['userid']})

@app.route("/login/pwfind", methods=["POST"])
def login_pw_find():
    l_pw_find_data1 = request.form['userId']
    l_pw_find_data2 = request.form['userName']
    l_pw_find_data3 = request.form['userEmail']
    pw_set = db.users.find_one({'userid':l_pw_find_data1}, {'_id': False})

    if (pw_set['username'] == l_pw_find_data2) and pw_set['useremail'] == l_pw_find_data3 :
        return jsonify({'msg': '비밀번호는 ' + pw_set['userpw'] + "입니다."})
    else:
        return jsonify({'msg': '정보를 다시확인해주세요.'})

@app.route('/mypage')
def mypage():
    return render_template('mypage.html')


    #영화 데이터베이스 클라이언트로 내려주기
@app.route("/boardGet", methods=["GET"])
def board_get():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)
        myId = payload['id'] # 내 아이디 가져오기

        myboard = list(db.dbuser_moviedata.find({'user_ID': myId}, {'_id': False})) # 내 아이디와 작성자가 같은 영화데이터 가져오기
        # user_moviedata(알수없음) dbmoviedata(영화갯수 데이터) dbuser_moviedata(전체 영화데이터) movie_arrindex

        moviechk = list(db.dbmoviedata.find({}, {'_id': False}))

        for moviechks in moviechk:
            arrchk = print(moviechks['movie_arrindex'])



        return jsonify({'myboard': myboard})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return redirect(url_for('home'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('home'))




    #회원 정보 데이터베이스 클라이언트로 내려주기
@app.route("/memberRead", methods=["GET"])
def member_read():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # print(payload)

        myinfo = db.users.find_one({'userid': payload['id']}, {'_id': 0})
        # print(myinfo)
        return jsonify({'myinfo': myinfo})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return redirect(url_for('home'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('home'))

    memberread = list(db.users.find({}, {'_id': False}))
    return jsonify({'memberread': memberread})


    # 개인정보 수정을 위한 로그인한 본인의 정보 데이터베이스 확인 및 수정
@app.route("/mypageInfo", methods=["POST"])
def user_update():
    # 개인정보 수정 요청온 값.
    memberName_receive = request.form['memberName_give']
    memberPhone_receive = request.form['memberPhone_give']
    memberEmail_receive = request.form['memberEmail_give']
    print(memberEmail_receive, memberPhone_receive, memberName_receive)

    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        myinfo = db.users.find_one({'userid': payload['id']}, {'_id': 0})
        print(myinfo)
        myname = myinfo['username']     # 나의 이름
        myphone = myinfo['userphone']   # 나의 전화번호
        myemail = myinfo['useremail']   # 나의 이메일
        print(myname, myphone, myemail, '나의 정보들')


        # 내 개인정보 찾아서 수정하기
        if (myname == "") is not None:
            db.users.update_one({'username': myname}, {'$set': {'username': memberName_receive}})
        if (myphone == "") is not None:
            db.users.update_one({'userphone': myphone}, {'$set': {'userphone': memberPhone_receive}})
        if (myphone == "") is not None:
            db.users.update_one({'useremail': myemail}, {'$set': {'useremail': memberEmail_receive}})

        myinfo = db.users.find_one({'userid': payload['id']}, {'_id': 0})
        print(myinfo)
        return jsonify({'msg': '수정 완료 !'})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return redirect(url_for('home'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('home'))
    return jsonify({'msg': '수정 완료 !'})


@app.route("/userDelete", methods=["POST"])
def user_delete():
    memberName_receive = request.form['userId_give']
    # print(memberName_receive, ' << 받아온 아이디값')
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # print(payload)

        myinfo = db.users.find_one({'userid': payload['id']}, {'_id': 0})
        # print(myinfo)
        myid = myinfo['userid']

        db.users.delete_one({'userid': myid})

        return jsonify({'msg': '회원 탈퇴 되었습니다. 감사합니다.'})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return redirect(url_for('home'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('home'))

@app.route("/titChk", methods=["POST"])
def user_movie_title():
    title_receive = request.form['title_give']
    print(title_receive)
    userMovieTit = list(db.dbmoviedata.find({'movie_title': title_receive}, {'_id': False}))
    print(userMovieTit)

    return jsonify({'arrIndexChk': userMovieTit})


@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/memaree')
def memup():
    return render_template('memaree.html')

def pagenation(db_collection,page_size, page_num):
    """returns a set of documents belonging to page number `page_num`
    where size of each page is `page_size`.
    """
    # Calculate number of documents to skip
    skips = page_size * (page_num - 1)

    # Skip and limit
    answer_list = list(db[db_collection].find({}, {'_id': False}).skip(skips).limit(page_size))

    # Return documents
    return answer_list


PAGE_SIZE_NUM = 10 # 1페이지당 게시글 수
MAX_PAGE_NUM = 10 # 몇 페이지 까지 만들 수 있는지

@app.route('/board/<cur_page_num>')
def board(cur_page_num):
# @app.route('/board')
# def board():
    total_movie_num = len(list(db['dbmoviedata'].find({}, {'_id': False})))

    # PAGE_SIZE_NUM = 10 # 1페이지당 게시글 수
    # MAX_PAGE_NUM = 10 # 몇 페이지 까지 만들 수 있는지
    PAGE_NUM = int(cur_page_num)

    pagenation_arr = [1]
    for i in range(1, MAX_PAGE_NUM+1) :
        if(total_movie_num / PAGE_SIZE_NUM > i):
            pagenation_arr.append(i+1)

    pagenation_arr_max = max(pagenation_arr)
    pagenation_arr_min = min(pagenation_arr)

    if (PAGE_NUM > ((total_movie_num / PAGE_SIZE_NUM)+1)) : # 현재 표시되는 최대 페이지 수보다 큰 페이지 수에 접근하면 표시되는 최대 페이지 수로 return
        jinja2_cur_page_num = pagenation_arr_max

    else :
        jinja2_cur_page_num = PAGE_NUM
    
    all_movies = pagenation('dbmoviedata',PAGE_SIZE_NUM,jinja2_cur_page_num)

    return render_template('board.html', all_movies = all_movies , pagenation_arr = pagenation_arr  , cur_page_num = jinja2_cur_page_num , pagenation_arr_max = pagenation_arr_max, pagenation_arr_min = pagenation_arr_min)

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
        userinfo = db.users.find_one({'userid': payload['id']}, {'_id': 0})
        return render_template('board_write.html',userid = userinfo['userid'])
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return redirect(url_for('login'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('login'))

@app.route('/board_detail/<keyword>')
def board_detail(keyword):
    moviedata = list(db.dbmoviedata.find({'movie_arrindex': int(keyword)}, {'_id': False}))[0] #get영화 정보
    userdatas = list(db.dbuser_moviedata.find({'movie_title': moviedata['movie_title']}, {'_id': False})) #get유저 정보
    all_movies = list(db.dbmoviedata.find({}, {'_id': False}))
    #글 번호
    total_movie_num = len(all_movies)
    cur_arrinex_num = moviedata['movie_arrindex']

    #넘어갈 목록 번호
    if(((cur_arrinex_num / PAGE_SIZE_NUM)+1) % 1 != 0) :
        goto_list_num = int((cur_arrinex_num / PAGE_SIZE_NUM)+1)
    else :
        goto_list_num = int((cur_arrinex_num / PAGE_SIZE_NUM))

    if(moviedata['movie_arrindex'] > 1) :
        pre_post = moviedata['movie_arrindex'] - 1
    elif(moviedata['movie_arrindex'] == 1) :
        pre_post = -1

    if(moviedata['movie_arrindex'] < total_movie_num) :
        next_post = moviedata['movie_arrindex'] + 1
    elif(moviedata['movie_arrindex'] == total_movie_num) :
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
                           userdatas = userdatas,
                           goto_list_num = goto_list_num,
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
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
            #서버와 로컬의 파이썬의 버전이 다르므로, 로컬에서 실행 시 아래 코드를 사용해야한다.
            # token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
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
        image = soup.select_one('meta[property="og:image"]')['content']

        user_moviedata = {
            'movie_title': title,
            'movie_img': image,
            'user_ID' : user_ID,
            'user_star' : int(star_receive),
            'user_comment': comment_receive,
        }
        # print(user_moviedata)
        db.dbuser_moviedata.insert_one(user_moviedata)

        # print(result)
        
        if result is not None: # 이미 영화 데이터가 존재
            totalsum = 0
            avg_star_string = ""
            #기존 DB 검색
            all_user_moviedata = list(db.dbuser_moviedata.find({'movie_title': title}, {'_id': False}))
            #추천 수 변경
            cur_recommand = len(all_user_moviedata)
            #평균 별점 변경
            for user_moviedata in all_user_moviedata :
                totalsum += user_moviedata['user_star']
            avg_star_string = "{:.1f}".format(totalsum / cur_recommand)  # 기존 데이터들의 별점 합 에다가 현재 추가 하려는 데이터의 별점 추가 후 나누기
            # print("avg_star_string",avg_star_string) # round 처리 해주기
            db.dbmoviedata.update_one({'movie_title': title}, {'$set': {'movie_recommand': cur_recommand}})
            db.dbmoviedata.update_one({'movie_title': title}, {'$set': {'movie_avg_star': float(avg_star_string)}})
        
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
            #영화 정보 크롤링 (img는 위에서 이미 처리함)
            desc = soup.select_one('meta[property="og:description"]')['content']
            releaseDates = soup.select(
                'div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(4) > a')

            if (len(releaseDates) == 0):
                releaseDate = ""
            else:
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

        return jsonify({'code': 10, 'msg': '등록되었습니다.'})

    else:
        return jsonify({'code': -99, 'msg': '정의되지 않은 요청코드'})





if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
