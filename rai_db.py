import psycopg2
import random
from collections import Counter
import time
import threading


class RaiDB:
    debuglist = []
    threadLock = threading.Lock()
    # conn = psycopg2.connect(database="postgresdb", user="david",
    #                         password="a123321a", host="192.168.50.100", port="5432")
    # # in docker
    conn = psycopg2.connect(database="postgresdb", user="david",
                            password="a123321a", host="193.168.44.15", port="5432")
    projectname = "fitfamilymart_"
    UserType_Table = projectname+"usertype"
    # http://192.168.50.100:8311/getImageUrl/Rai辦公室_1643092200.8617697.avi
    zoomtime = 28800

    def create_table(self, conn, tablename, tabletype):
        # 創建表
        cur = conn.cursor()
        sqlStr = 'CREATE TABLE  '+tablename+' (ID  SERIAL PRIMARY KEY,'
        for item in tabletype:
            sqlStr = sqlStr + item['name'] + " " + \
                item['type'] + " " + item['NULL'] + ","
        sqlStr = sqlStr[:-1] + ");"
        try:
            cur.execute(sqlStr)
            print("Table created successfully")
        except Exception as e:
            print("資料表已存在")
        self.conn.commit()

    def delete_data_id(self, tablename, cur, sn):
        cur.execute(cur.mogrify('DELETE FROM ' +
                    tablename+' WHERE id = '+str(sn)))
        self.conn.commit()

    def add_data_by_dict(self, tablename, cur, d, commit=True):
        KEYS = d.keys()
        COLUMNS = ','.join(KEYS)
        VALUES = ','.join(['%({})s'.format(k) for k in KEYS])
        INSERT = 'insert into '+tablename + \
            ' ({0}) values ({1}) RETURNING ID'.format(COLUMNS, VALUES)
        sql = cur.mogrify(INSERT, d)
        cur.execute(sql)
        hundred = cur.fetchone()[0]
        if commit:
            self.conn.commit()
        return hundred

    def update_data_by_dict(self, tablename, cur, d, wname, nvalue):
        # cur.execute("UPDATE Class SET Attendance=1 WHERE key = \'1631264035_679811\'")
        KEYS = d.keys()
        for k in KEYS:
            cur.execute("UPDATE "+tablename+" SET "+k+"=\'" +
                        str(d[k])+"\' WHERE "+wname+" = \'"+nvalue+"\'")
        self.conn.commit()

    def timestampToString(self, timestamp):
        struct_time = time.localtime(timestamp+self.zoomtime)  # 轉成時間元組
        timeString = time.strftime("%Y-%m-%d %H:%M:%S", struct_time)  # 轉成字串
        return timeString

    def getConn(self):
        try:
            cur = self.conn.cursor()
        except:
            self.conn = psycopg2.connect(database="postgresdb", user="david",
                                         password="a123321a", host="193.168.44.15", port="5432")
            cur = self.conn.cursor()
        return cur
    


    def addType(self, userid, type,p):
        '''新增使用者類型'''
        self.threadLock.acquire()
        try:
            cur = self.getConn()
            classid = self.add_data_by_dict(self.UserType_Table, cur, {
                "userid": userid, "createtime": self.timestampToString(time.time()), 'type': type,"p":p})
            self.conn.commit()
        except:
            self.conn.commit()
        self.threadLock.release()
        return classid

    def __init__(self) -> None:
        tabletype = list()
        tabletype.append(
            {"name": "userid", "type": "character (18)", "NULL": "NOT NULL"})
        tabletype.append(
            {"name": "createtime", "type": " timestamp", "NULL": "NOT NULL"})
        tabletype.append(
            {"name": "type", "type": "text", "NULL": "NOT NULL"})
        tabletype.append(
            {"name": "p", "type": "numeric", "NULL": "NOT NULL"})
            
        self.create_table(self.conn, self.UserType_Table, tabletype)