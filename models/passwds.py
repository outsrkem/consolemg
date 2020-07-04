#-*- coding=utf-8 -*-
from flask import session
from sqlalchemy import Table
from common.database import dbconnect

dbsession, md, DBase = dbconnect()


class Passwds(DBase):
    __table__ = Table('passwd', md, autoload=True)