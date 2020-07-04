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




    # 查询用户
    def find_by_username(self, USERNAME):
        result = dbsession.query(Users).filter_by(USERNAME=USERNAME).all()
        return result

    # 根据用户名获取密码
    def find_by_passwd(self, username):
        result = dbsession.query(Passwds).join(Users, Passwds.USERID == Users.USERID).filter(Users.USERNAME == username).first()
        return result

    # 根据用户名获取用户信息
    def find_by_userinfo(self, username):
        result = dbsession.query(Users, Passwds).join(Users,Passwds.USERID==Users.USERID).filter(Users.USERNAME==username).first()
        result = model_list(result)[0]
        return result


    # 插入注册用户名
    def inst_user(self, userid, username, ):
        user = Users(USERID=userid, USERNAME=username, ROLE='1')
        dbsession.add(user)
        dbsession.commit()
        return user

    # 插入注册用户密码
    def inst_passwd(self, userid, passwd):
        nowtime = time.strftime('%Y-%m-%d %H:%M:%S')
        inactive = Caltime(time.strftime('%Y-%m-%d'))
        dbsession.add(Passwds(USERID=userid, PASSWD=passwd,CHANGE = nowtime,INACTIVE = '0'))
        dbsession.commit()

    # 分装用户注册模型
    def user_register(self, userid, username, passwd):
        user = self.inst_user(userid, username)
        self.inst_passwd(userid, passwd)
        return user

    # 修改密码
    def change_passwd(self, userid, passwd):
        nowtime = time.strftime('%Y-%m-%d %H:%M:%S')
        inactive = Caltime(time.strftime('%Y-%m-%d'))
        row = dbsession.query(Passwds).filter_by(USERID=userid).first()
        row.PASSWD = passwd
        row.CHANGE = nowtime
        row.INACTIVE = inactive + 180
        dbsession.commit()
        return 'change_passwd_pass'


if __name__ == '__main__':
    aa = Users
