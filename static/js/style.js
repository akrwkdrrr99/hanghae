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