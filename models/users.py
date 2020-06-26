#-*- coding=utf-8 -*-
from flask import session
from sqlalchemy import Table
from common.database import dbconnect
from models.passwd import Passwd
import time, random

dbsession, md, DBase = dbconnect()


class Users(DBase):
    __table__ = Table('user', md, autoload=True)

    def find_by_username(self, USERNAME):
        result = dbsession.query(Users).filter_by(USERNAME=USERNAME).all()
        return result

    def find_passwd(self, USERID):
        result = dbsession.query(Passwd).filter_by(USERID=USERID).all()
        print(result)
        return result

if __name__ == '__main__':
    aa= Users
    aa().find_passwd(USERID='1')