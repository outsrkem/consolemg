# -*- coding=utf-8 -*-
from sqlalchemy import Table
from common.database import dbconnect
import time
from common.utility import model_list
from common.function import Caltime

dbsession, md, DBase = dbconnect()


class Passwds(DBase):
    __table__ = Table('passwd', md, autoload=True)


class Users(DBase):
    __table__ = Table('user', md, autoload=True)

    # 查询用户信息
    def find_by_userinfo(self, username):
        result = dbsession.query(Users).filter_by(USERNAME=username).all()
        return result

    # 根据用户名获取密码信息
    def find_by_passwdinfo(self, username):
        result = dbsession.query(Passwds).join(Users, Passwds.USERID == Users.USERID).filter(Users.USERNAME == username).first()
        return result

    # 插入注册用户名
    def inst_user(self, userid, username, email):
        # user = Users(USERID=userid, USERNAME=username, ROLE='1')
        try:
            dbsession.add(Users(USERID=userid, USERNAME=username, EMAIL=email, ROLE='1'))
            dbsession.commit()
            return 'inst-u-pass'
        except Exception as e:
            print("异常:[%s] [%s] [%s]" % (e.__traceback__.tb_lineno, e.__traceback__.tb_frame.f_globals['__file__'], e))
            return 'inst-u-failed'

    # 插入注册用户密码
    # 如果密码插入失败，则删除刚插入的改用户信息
    # INACTIVE='0' 为第一次注册，登录则提示修改密码
    def inst_passwd(self, userid, passwd):
        try:
            nowtime = time.strftime('%Y-%m-%d %H:%M:%S')
            # inactive = Caltime(time.strftime('%Y-%m-%d'))
            dbsession.add(Passwds(USERID=userid, PASSWD=passwd, CHANGE=nowtime, INACTIVE='0'))
            dbsession.commit()
            return 'inst-p-pass'
        except Exception as e:
            dbsession.query(Users).filter_by(USERID=userid).delete()
            dbsession.commit()
            print("异常:[%s] [%s] [%s]" % (e.__traceback__.tb_lineno, e.__traceback__.tb_frame.f_globals['__file__'], e))
            return 'inst-p-failed'

    # 分装用户注册模型
    # 用户信息插入成功，才能执行插入密码inst_passwd，如果密码插入失败，则删除刚插入的改用户信息
    def user_register(self, userid, username, passwd, email):
        row_u = self.inst_user(userid, username, email)
        if row_u == 'inst-u-pass':
            row_p = self.inst_passwd(userid, passwd)
            if row_p == 'inst-p-pass':
                return 'inst-pass'
            else:
                return 'inst-failed'
        else:
            return 'inst-failed'

    # 修改密码，密码从当天增加有效期180天
    def change_passwd(self, userid, passwd):
        nowtime = time.strftime('%Y-%m-%d %H:%M:%S')
        inactive = Caltime(time.strftime('%Y-%m-%d'))
        row = dbsession.query(Passwds).filter_by(USERID=userid).first()
        row.PASSWD = passwd
        row.CHANGE = nowtime
        row.INACTIVE = inactive + 180
        dbsession.commit()
        return 'change_passwd_pass'

    # 删除用户
    def delete_user(self, userid):
        dbsession.query(Users).filter_by(USERID=userid).delete()
        dbsession.commit()
        dbsession.query(Passwds).filter_by(USERID=userid).delete()
        dbsession.commit()
        return 'cancel-pass'
