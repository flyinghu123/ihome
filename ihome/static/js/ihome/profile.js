function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(document).ready(function () {
    $('#form-avatar').submit(function(e) {
        e.preventDefault();
        //利用jquery.form.min.js提供的ajaxSubmit对表单进行异步提交
        $(this).ajaxSubmit({
            url: '/api/v1.0/users/avatar',
            type: 'post',
            dataType: 'json',
            headers: {
                'X-CSRFToken': getCookie("csrf_token")
            },  //请求头, 将csrf_token值放到请求头中, 方便后端csrf进行验证
            success: function (resp) {
                if (resp.errno == '0') {
                    //上传成功
                    $('#user-avatar').attr('src', resp.data.avatar_url);
                } else {
                    alert(resp.errmsg);
                }
            }
        })
    });
})