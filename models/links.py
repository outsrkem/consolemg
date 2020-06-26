#-*- coding=utf-8 -*-
from flask import session
from sqlalchemy import Table
from common.database import dbconnect


dbsession, md, DBase = dbconnect()


class Links(DBase):
    __table__ = Table('links', md, autoload=True)

    def find_by_links(self):
        result = dbsession.query(Links).all()
        return result

if __name__ == '__main__':
    row=Links().find_by_links()
    print(row)
    for i in row:
        print(i.LINKNAME, i.LINKURL)