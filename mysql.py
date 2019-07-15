import pymysql
class Mysql:
    def __init__(self,dbName):
        self.db = pymysql.connect("127.0.0.1", "root", "",dbName)
        self.cursor = self.db.cursor()
        print("连接成功")
    def getdata(self):
        return self.cursor.fetchall()

    def excutesql(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print("异常:",str(e))
            self.db.rollback()
        else:
            print("成功:",sql)