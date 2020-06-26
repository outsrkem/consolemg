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
                location.href = '/aaa';
            }, 200);
        } else if (data == "login-error") {
            alert("登录失败，请检查用户名或密码是否正确。")
        } else {
            alert(param)
        }
    });
}