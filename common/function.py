import datetime
import time
def Caltime(date2):
    date1 = '1970-01-01'
    date1=time.strptime(date1,"%Y-%m-%d")
    date2=time.strptime(date2,"%Y-%m-%d")
    date1=datetime.datetime(date1[0],date1[1],date1[2])
    date2=datetime.datetime(date2[0],date2[1],date2[2])
    print((date2-date1).days)#将天数转成int型
    return (date2-date1).days