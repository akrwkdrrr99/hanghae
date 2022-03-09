document.addEventListener("DOMContentLoaded", function () {
    const hd = document.getElementById('hd');
    const bodySet = document.querySelector("body");

    // 팝업관련
    if( document.querySelector(".p_close")) {
        const popUpClose = document.querySelector(".p_close");
        const popUpArea = document.querySelector(".popup_area");
        const id_find_bt = document.querySelector('.id_find');
        const pw_find_bt = document.querySelector('.pw_find');
        const popBox = document.querySelectorAll('.pop_up_box > div');
        const id_find_box = document.querySelector('.findIdPopUp');
        const pw_find_box = document.querySelector('.findpwPopUp');
        let popUpName = "";
        let popUpSet = "";

        const p_open_init = function(e) {
            e.preventDefault();
            bodySet.classList.add("setof");
            popUpClose.parentNode.style.opacity = "1";
            popUpArea.classList.add("show");
        };

        const p_close_init = function() {
            for(let i = 0; i <popBox.length; i++) {
                popBox[i].style.display="none";
            };
        };

        const p_close_f = function(e) {
            e.preventDefault();
            this.parentNode.style.opacity = "0";
            this.parentNode.parentNode.classList.remove("show");
            bodySet.classList.remove("setof");
            p_close_init();
        };

        id_find_bt.addEventListener('click', function(e) {
            e.preventDefault();
            p_open_init(e);
            popUpName = "." + this.className + "_PopUp";
            popUpSet = document.querySelector(popUpName);
            popUpSet.style.display = "block";
        })

        pw_find_bt.addEventListener('click', function(e) {
            e.preventDefault();
            p_open_init(e);
            popUpName = "." + this.className + "_PopUp";
            popUpSet = document.querySelector(popUpName);
            popUpSet.style.display = "block";
        })

        popUpClose.addEventListener('click', p_close_f);
    } else {

    }

});


// mypage script

$(function () {
    pageChk = $('.mypageInner').length;
    if (pageChk >= 1) {
        // 회원탈퇴 확인 팝업창
        $('.withdrawalBtn').click(function () {
            $('.withdrawalModal').show();
        })

        $('.withdrawalCloseBtn').click(function () {
            $('.withdrawalModal').hide();
        })

        // 프로필 수정 팝업창
        $('.updateBtn').click(function () {
            $('.updateModal').show();
        })

        $('.updateModalCloseBtn').click(function () {
            $('.updateModal').hide();

        })

    }
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

function enter_board() {
    window.location.href="/board"
}

function enter_board_detail(index) {
    $.ajax({
        type: 'GET',
        url: `/board_detail/${index}`,
        data: {},
        success: function (response) {
            window.location.href=`/board_detail/${index}`
        }
    });
}

function move_board_detail(index) {
    if (index != -1 && index != -2) {
        $.ajax({
            type: 'GET',
            url: `/board_detail/${index}`,
            data: {},
            success: function (response) {
                window.location.href = `/board_detail/${index}`
            }
        });
    }
    else if (index == -1) {
        alert("첫번째 글입니다.")
        
    }else if(index == -2){
        alert("마지막 글입니다.")
    }
}

//Get the button:
mybutton = document.getElementById("myBtn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}
