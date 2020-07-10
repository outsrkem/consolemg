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
        } else if (data == 'For-the-first-time-login') {
            // alert("首次登陆，请重置密码。");
            var click = confirm("首次登陆，点击确定，修改密码。");
            if (click) {
                window.location.href = "/chpasswd";
            } else {
                console.log("点击了取消，无动作" + click);
            }


        } else {
            alert("系统异常，请联系管理员。");
        }
    });
}

/**
 * 修改密码
 */
function dochpasswd(e) {
    if (e != null && e.keyCode != 13) {
        return false;
    }

    var inlodpass = $.trim($("#inlodpass").val());
    var innewpass = $.trim($("#innewpass").val());
    // 构建POST请求的正文数据
    param = "oldpassword=" + inlodpass;
    param += "&newpassword=" + innewpass;
    // 利用jQuery框架发送POST请求，并获取到后台登录接口的响应内容
    $.post('/chpasswd', param, function (data) {
        if (data == "change-password-pass") {
            alert("密码修改成功");
        } else if (data == "auth-failure") {
            alert("密码认证错误。");
        } else if (data == 'error') {
            alert("请求错误");
        } else {
            alert("系统异常，请联系管理员。");
        }
    });
}


function canceluser(userid) {
    var mcode = $.trim($("#mcode").val());
    //ajax没有delete请求，使用ajax发送任何形式的请求（原生方式）
    $.ajax({
        url: '/deluser/' + userid,
        data: {_method: "DELETE", mcode: mcode},
        type: 'POST',
        success: function (data) {
            if (data == 'cancel-pass') {
                alert("账号已成功注销。");
            } else if (data == 'mcode-error') {
                alert("验证码错误。");
            } else {
                alert("系统异常，请联系管理员。");
            }
        }
    });
}

/**
 * 发送邮件验证码
 * @param obj
 * @returns {boolean}
 */
function doSendMail(obj) {

    var email = $.trim($("#regemail").val());
    $(obj).attr('disabled', true);     // 发送邮件按钮变成不可用
    $.post('/ecode', function (data) {
        if (data == 'send-pass') {
            alert("验证码已成功发送到邮箱 < " + email + " > 请查收。")
            return false;
        } else {
            alert("邮箱验证码发送失败。请稍后重试。")
            return false;
        }
    });
}