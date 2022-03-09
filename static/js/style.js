document.addEventListener("DOMContentLoaded", function () {
    const hd = document.getElementById('hd');
    const menu_bt = document.querySelector('.menu_bt');
    const pw_find_bt = document.querySelector('.pw_find_btn');
    //const pw_find_box = document.querySelector('.pw_find_box');
    menu_bt.addEventListener('click', function (e) {
        e.preventDefault();
        this.classList.toggle('on');
    })


    pw_find_bt.addEventListener('click', function (e) {
        e.preventDefault();
        pw_find_box.classList.toggle('on');
    })


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

        $('.updateModalCloseBtn').click(function(){
            $('.updateModal').hide();

        })

    }







}) // mypage script end
