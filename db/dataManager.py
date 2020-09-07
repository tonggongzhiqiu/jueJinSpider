import pymysql
import threading
import pandas as pd
import numpy as np
from jueJin.db.settings import MYSQL_HOST, MYSQL_DB, MYSQL_PWD, MYSQL_USER


class DataManager():
    # 单例模式，确保每次实例化都调用一个对象
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(DataManager, "_instance"):
            with DataManager._instance_lock:
                DataManager._instance = object.__new__(cls)
                return DataManager._instance

    def __init__(self):
        # 建立连接
        self.conn = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PWD, MYSQL_DB, charset="utf8")
        # 建立游标
        self.cursor = self.conn.cursor()

    def saveBriefInfo(self, data):
        """
            功能：保存内容信息
            @param data: 元组类型
        """
        # 定义一个 sql 语句
        sql = "insert into briefinfo(title, userName, briefContent, linkUrl) values(%s,%s,%s,%s)"
        # 准备数据
        try:
            self.cursor.execute(sql, data)
            self.conn.commit()
            print("插入成功")
        except Exception as e:
            print("插入数据失败", e)
            # 回滚
            self.conn.rollback()

    def saveContent(self, data):
        """
        功能：保存内容信息
        在这部分的数据库中，由于 content 过长，将数据库 content.type 定义为 LongText
        @param data: 元组类型
        """
        # 数据库操作
        # 定义一个 sql 语句
        sql = "insert into content(title, content) values(%s,%s)"
        # 准备数据
        try:
            self.cursor.execute(sql, data)
            self.conn.commit()
            print("插入成功")
        except Exception as e:
            print("插入数据失败", e)
            # 回滚
            self.conn.rollback()

    def getData(self) -> object:
        """
        功能：这部分从 briefinfo 表格拿出 link，并以 list 形式返回
        @return: [["https://juejin.im/post/6844904144533192717"]]
        """
        sql = "SELECT linkUrl FROM briefinfo"
        try:
            # 使用 pd 模块执行操作，并最终转换为 list 形式
            df = pd.read_sql(sql, self.conn)
            df1 = np.array(df)
            df3 = df1.tolist()
        except Exception as e:
            print("", e)
        return df3

    def __del__(self):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()
