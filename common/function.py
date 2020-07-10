import datetime
import time
import base64
import hmac
import hashlib
import cryptography.fernet


def Caltime(date2):
    date1 = '1970-01-01'
    date1 = time.strptime(date1, "%Y-%m-%d")
    date2 = time.strptime(date2, "%Y-%m-%d")
    date1 = datetime.datetime(date1[0], date1[1], date1[2])
    date2 = datetime.datetime(date2[0], date2[1], date2[2])
    # 将天数转成int型
    return (date2 - date1).days


def generate_token(key, expire):
    r'''
        @Args:
            key: str (用户给定的key，需要用户保存以便之后验证token,每次产生token时的key 都可以是同一个key)
            expire: int(最大有效时间，单位为s)
        @Return:
            state: str
    '''
    ts_str = str(time.time() + int(expire))
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr = hmac.new(key.encode("utf-8"), ts_byte, 'sha1').hexdigest()
    token = ts_str + ':' + sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")


def certify_token(key, token):
    r'''
        @Args:
            key: str
            token: str
        @Returns:
            boolean
    '''
    token_str = base64.urlsafe_b64decode(token).decode('utf-8')
    token_list = token_str.split(':')
    if len(token_list) != 2:
        return False
    ts_str = token_list[0]
    if float(ts_str) < time.time():
        # token expired
        return False
    known_sha1_tsstr = token_list[1]
    sha1 = hmac.new(key.encode("utf-8"), ts_str.encode('utf-8'), 'sha1')
    calc_sha1_tsstr = sha1.hexdigest()
    if calc_sha1_tsstr != known_sha1_tsstr:
        # token certification failed
        return False
    # token certification success
    return True


def sha256hex(data):
    sha256 = hashlib.sha256()
    sha256.update(data.encode())
    res = sha256.hexdigest()
    return res


def encrypt_userid(data):
    a = cryptography.fernet.Fernet.generate_key()  # 自动生成密钥
    b = cryptography.fernet.Fernet(a)
    c = b.encrypt(data.encode())  # 使用生成的密钥加密
    return c


def decode_userid(data, b):
    d = b.decrypt(data)  # 使用生成的密钥解密
    res = d.decode()
    return res


from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
import random, string

def send_email(receiver, ecode):
    sender = 'Yonge <xhdascnf@126.com>'
    # receivers = ['429240967@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    content = f"<br/>欢迎注册博客，验证码为：" \
              f"<span style='color: red; font-size: 20px;'>{ecode}</span><br/> " \
              f"请复制到注册窗口完成注册，感谢您的支持。<br/>"
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(content, 'html', 'utf-8')
    message['Subject'] = Header('博客验证码', 'utf-8')
    message['From'] = sender  # 发送者
    message['To'] = receiver  # 接收者

    subject = 'Python SMTP 邮件测试'

    smtpObj = SMTP_SSL('smtp.126.com')
    smtpObj.login(user='xhdascnf@126.com', password='HKFKVIQTMAWGGBVD')
    smtpObj.sendmail(sender, receiver, str(message))
    smtpObj.quit()


# 生成6位随机邮箱验证码
def gen_email_code():
    str = random.sample(string.ascii_letters + string.digits, 6)
    # str = 'asdasd'
    return ''.join(str)
