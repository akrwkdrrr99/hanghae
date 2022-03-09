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
