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
            setTimeout(function () {
                location.href = '/usercenter';
            }, 200);
        } else if (data == "auth-failure") {
            alert("密码认证错误。");
        } else if (data == 'error') {
            alert("请求错误");
        } else if(data == 'passwd-invalid') {
            alert("密码过于简单。");
        } else {
            alert("系统异常，请联系管理员。");
        }
    });
}

/**
 * 用户账号注销
 * @param mcode
 */
function canceluser() {
    var mcode = $.trim($("#mcode").val());
    //ajax没有delete请求，可使用ajax原生方式发送任何形式的请求
    var click = confirm("确定要注销账号吗？注销之后不可恢复。");
    if (click) {
        $.ajax({
            url: '/deluser',
            data: {_method: "DELETE", mcode: mcode},
            type: 'DELETE',
            success: function (data) {
                if (data == 'cancel-pass') {
                    alert("账号已成功注销。");
                    setTimeout(function () {
                        location.href = '/login';
                    }, 200);
                } else if (data == 'mcode-error') {
                    alert("验证码错误。");
                } else {
                    alert("系统异常，请联系管理员。");
                }
            }
        });
    } else {
        console.log("点击了取消");
    }

}

/**
 * 发送邮件验证码
 * @param obj
 * @returns {boolean}
 */
function doSendMail(e) {
    var email = $.trim($("#regemail").val());
    t = setInterval(function () {
        countdown(e)
    }, 1000)
    countdown(e);
    $.post('/ecode', function (data) {
        if (data == 'send-pass') {
            // 移除验证码发送提示。
            $("#appendcontent").empty();
            $("#appendcontent").append("验证码已成功发送到邮箱 < " + email + " > 请查收。");
            console.log("验证码已成功发送到邮箱 < " + email + " > 请查收。");
            return false;
        } else {
            alert("邮箱验证码发送失败。请稍后重试。")
            return false;
        }
    });
}

/**
 * 倒计时
 */
var t; //倒计时对象
var time = 10;

function countdown(e) {
    if (time == 0) {
        //这里时设置当时间到0的时候重新设置点击事件，并且默认time修改为60
        e.setAttribute("onclick", "doSendMail(this)");
        $(e).attr('disabled', false);
        document.getElementById("getcode").innerText = "获取验证码";
        time = 10;
        clearInterval(t);
    } else {
        //这里是显示时间倒计时的时候点击不生效
        // e.setAttribute("onclick", '');
        $(e).attr('disabled', true);
        document.getElementById("getcode").innerHTML = time + " 秒后重试";
        time--;
    }
}