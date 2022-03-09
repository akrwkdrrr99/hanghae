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

    if(star == "-- 선택하기 --"){
        alert("평점을 선택해주세요")
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