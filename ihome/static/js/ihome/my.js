function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function logout() {
    $.ajax({
            url: '/api/v1.0/session',
            type: 'delete',
            headers: {
                'X-CSRFToken': getCookie("csrf_token")
            },  //请求头, 将csrf_token值放到请求头中, 方便后端csrf进行验证
            success: function (resp) {
                if (resp.errno == '0') {
                    //注册成功跳转主页
                    location.href = '/index.html';
                }
            }
        })
}

$(document).ready(function(){
})