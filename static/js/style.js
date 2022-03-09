document.addEventListener("DOMContentLoaded", function(){
    const hd = document.getElementById('hd');
    const menu_bt = document.querySelector('.menu_bt');
    const pw_find_bt = document.querySelector('.pw_find_btn');
    //const pw_find_box = document.querySelector('.pw_find_box');
    menu_bt.addEventListener('click', function(e) {
        e.preventDefault();
        this.classList.toggle('on');
    })

    pw_find_bt.addEventListener('click', function(e) {
        e.preventDefault();
        pw_find_box.classList.toggle('on');
    })
});

function posting() {
    let user_ID = $('#user_ID').val()
    let url = $('#url').val()
    let star = $('#star').val()
    let comment = $('#comment').val()

    if(user_ID == ""){
        alert("ID를 입력해주세요")
        return
    }
    else if(url == ""){
        alert("영화URL을 입력해주세요")
        return
    }
    else if(star == "-- 선택하기 --"){
        alert("평점을 선택해주세요")
        return
    }
    else if(comment == ""){
        alert("추천 이유를 입력해주세요")
        return
    }

    // indexOf : 해당 문자열로 시작 하면 시작하는 index값을 return, 없으면 -1 return
    if (url.indexOf("https://movie.naver.com/movie/bi/mi/basic.naver?code=") >= 0) {
        // alert("옳은 주소 입니다.")
    }
    else{
        alert("잘못된 주소 입니다. 네이버 영화에서 영화를 검색해주세요. (＃https:// 붙여주세요.)")
        return
    }

    $.ajax({
        type: 'POST',
        url: '/api',
        data: {reqType : 'postMovieData',user_ID_give : user_ID ,url_give: url, star_give: star, comment_give:comment},
        success: function (response) {
            alert(response['msg'])
            // window.location.reload()
        }
    });
}

function enter_board_write() {
    window.location.href="/board_write"
}

function close_box() {
    window.location.href="/"
}