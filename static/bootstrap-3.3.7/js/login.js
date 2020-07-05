/**
 * 登录处理
 */
function doLogin(e) {
    if (e != null && e.keyCode != 13) {
        return false;
    }

    var loginname = $.trim($("#loginname").val());
    var loginpass = $.trim($("#loginpass").val());
    // 构建POST请求的正文数据
    param = "username=" + loginname;
    param += "&password=" + loginpass;
    // 利用jQuery框架发送POST请求，并获取到后台登录接口的响应内容
    $.post('/login', param, function (data) {
        if (data == "login-pass") {
            setTimeout(function () {
                location.href = '/overview';
            }, 200);
        } else if (data == "login-error") {
            alert("登录失败，请检查用户名或密码是否正确。");
        } else if (data == 'password-expired') {
            alert("密码已失效，请重置密码。");
        } else if (data == 'For-the-first-time-login'){
            // alert("首次登陆，请重置密码。");
            var click = confirm("首次登陆，点击确定，修改密码。");
            if (click) {
                console.log("点击了确定，正在跳转"+click);
            } else {
                console.log("点击了取消，无动作"+click);
            }


        } else {
            alert("系统异常，请联系管理员。");
        }
    });
}