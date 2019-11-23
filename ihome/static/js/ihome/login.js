function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}
// 保存图片验证码编号
var imageCodeId = "";

function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}

function generateImageCode() {
    // 形成图片验证码的后端地址, 设置到页面中, 让浏览器请求验证码图片
    // 1. 生成图片验证码编号
    imageCodeId = generateUUID();
    // 图片url
    var url = '/api/v1.0/image_codes/' + imageCodeId;
    $('.image-code img').attr('src', url);
}

$(document).ready(function() {
    generateImageCode();

    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
    });
    $(".form-login").submit(function(e){
        e.preventDefault();
        var imageCode = $("#imagecode").val();
        var mobile = $("#mobile").val();
        var passwd = $("#password").val();
        if (!imageCode || imageCode.length != 4) {
            $("#image-code-err span").html("请填写正确验证码！");
            $("#image-code-err").show();
            return;
        }
        var mobileReg=/^[1][3,4,5,7,8][0-9]{9}$/;
        if (!mobileReg.test(mobile)) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        } 
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }
        //请求数据
        var req_data = {
            "image_code": imageCode,  // 图片验证码值
            "image_code_id": imageCodeId,  // 验证码编号
            'mobile': mobile,
            'password': passwd
        }
        //将请求数据转化为json
        var req_json = JSON.stringify(req_data);
        $.ajax({
            url: '/api/v1.0/sessions',
            type: 'post',
            dataType: 'json',
            data: req_json,
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': getCookie("csrf_token")
            },  //请求头, 将csrf_token值放到请求头中, 方便后端csrf进行验证
            success: function (resp) {
                if (resp.errno == '0') {
                    //注册成功跳转主页
                    location.href = '/index.html';
                } else {
                    // 其他错误信息, 在页面中展示
                    $("#password-err span").html(resp.errmsg);
                    $("#password-err").show();
                }
                 //刷新验证码
                generateImageCode();
            }
        })
    });
})