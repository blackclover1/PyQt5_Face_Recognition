import sqlite3 as db
import numpy as np


class Operate_Sql():
    def __init__(self):
        self.DB_Path = '../DB/FileNameDB.db'
        self.New_DB_Path = '../DB/StudentCheckWork.db'
        self.sqlStr_SelectAll = "select * from fileName;"
        self.sqlStr_InsertNewName = "insert into fileName(fName) values ("
        self.sqlStr_count = " select count(*) from fileName;"

    def readFronSqllite(self, db_path, exectCmd):
        conn = db.connect(db_path)  # 该 API 打开一个到 SQLite 数据库文件 database 的链接，如果数据库成功打开，则返回一个连接对象
        cursor = conn.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
        conn.row_factory = db.Row  # 可访问列信息
        cursor.execute(exectCmd)  # 该例程执行一个 SQL 语句
        rows = cursor.fetchall()  # 该例程获取查询结果集中所有（剩余）的行，返回一个列表。当没有可用的行时，则返回一个空的列表。
        conn.close()
        return rows

    # 构建sql插入语句
    def CreatSqlStr(self, fileName):
        str = self.sqlStr_InsertNewName + "'" + fileName + "');"
        return str

    # 查询所有信息
    def Select_All_Name(self):
        num = self.Num_Now_All()
        rows = self.readFronSqllite(self.DB_Path, self.sqlStr_SelectAll)
        readLines = num
        lineIndex = 0
        while lineIndex < readLines:
            row = rows[lineIndex]  # 获取某一行的数据,类型是tuple
            print(row[0], row[1], row[2])
            lineIndex += 1

    # 查询第一条信息
    def SelcetFirst(self):
        rows = self.readFronSqllite(self.DB_Path, self.sqlStr_SelectAll)
        readLines = 1
        lineIndex = 0
        while lineIndex < readLines:
            row = rows[lineIndex]  # 获取某一行的数据,类型是tuple
            print('第一条数据是：', row[0], row[1], row[2], '\n')
            lineIndex += 1

    # 返回所有行数
    def Num_Now_All(self):
        num_all = self.readFronSqllite(self.DB_Path, self.sqlStr_count)
        return (num_all[0][0])

    # 插入一条信息
    def Insert_New_Name(self, filename):
        conn = db.connect(self.DB_Path)  # 该 API 打开一个到 SQLite 数据库文件 database 的链接，如果数据库成功打开，则返回一个连接对象
        conn.execute(filename)
        conn.commit()
        print("插入完成\n")
        conn.close()

    # 查询是否存在相同的文件名
    def Select_Same_Name(self, name):
        rows = self.readFronSqllite(self.DB_Path, 'select * from fileName where fName ="' + str(name) + '";')
        if len(rows) == 0 or rows is None:  # 如果不存在相同名字的文件夹返回假
            # print(rows)
            print("不存在")
            return False
        else:  # 存在相同名字的文件夹返回真
            # print(len(rows))
            print("存在")
            # row = rows[0]  # 获取某一行的数据,类型是tuple
            # print('数据是：', row[0], row[1], '\n')
            return True

    def Delete_File_Name(self, filename):
        conn = db.connect(self.DB_Path)  # 该 API 打开一个到 SQLite 数据库文件 database 的链接，如果数据库成功打开，则返回一个连接对象
        filename = 'delete from fileName where fName="' + filename + '";'
        print(filename)
        conn.execute(filename)
        conn.commit()
        print("删除完成")
        conn.close()

    # 插入embadding
    def insert_emb(self, fname, emb):
        list_emb = []
        str_emb = ''
        for i in range(128):
            list_emb.append(str(emb[i]))  # 加入到list
            str_emb = str_emb + ' ' + list_emb[i]  # list转str
        sql_find = 'select * from fileName where fName="' + fname + '";'
        sql_update_emb = 'update fileName set flag=1, embadding= "' + str_emb + '" where fName="' + fname + '";'
        sql_insert_emb = 'insert into fileName(fName,flag,embadding) values ("' + fname + '",1,"' + str_emb + '");'
        conn = db.connect(self.DB_Path)
        rows = self.readFronSqllite(self.DB_Path, sql_find)  # 查询这个fname有没有embadding

        if len(rows) == 0 or rows is None:  # 如果不存在相同名字的文件夹返回假
            print("不存在")
            conn.execute(sql_insert_emb)
            conn.commit()
            print("插入完成\n")
            conn.close()
        else:
            print('存在')
            row = rows[0]
            print(row)
            # if len(row[1]) == 0: #or row[2] is None:  # 当前label没有embadding，直接插入embadding
            print('没有embadding')
            conn.execute(sql_update_emb)
            conn.commit()
            print("插入完成\n")
            conn.close()

    def get_sql_emb(self):
        list_emb = []
        emb_temp = np.zeros(128)
        num = self.Num_Now_All()
        emb_arr = np.zeros([num, 128])
        name = []
        str_emb = np.empty([num, 128], dtype=float)

        # 获取所有行
        rows = self.readFronSqllite(self.DB_Path, self.sqlStr_SelectAll)
        lineIndex = 0
        if len(rows) == 0 or rows == '':
            emb_arr = 0
        else:
            while lineIndex < num:
                row = rows[lineIndex]  # 获取某一行的数据,类型是tuple
                # print(row[0])
                name.append(row[0])  # 获取名字
                if row[1] == 0:
                    emb_arr[lineIndex] = np.full((1, 128), 10)
                else:
                    str_to_list = row[2].split()  # 以空格分割字符串
                    for i in range(128):
                        emb_arr[lineIndex][i] = float(str_to_list[i])  # 'list转ndarray:'，str->float
                lineIndex += 1

        return name, emb_arr, num

    # 删除班级表
    def delete_pc_table(self, profession, class_):
        table = profession + class_
        # 先检查是否存在这个表
        sql = "SELECT COUNT(*) FROM sqlite_master where type='table' and name='{str}';".format(str=table)
        conn = db.connect(self.New_DB_Path)
        cursor = conn.cursor()
        conn.row_factory = db.Row
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows[0][0] == 0:
            print('不存在这个表')
            return False
        sql_drop = 'drop table {table}'.format(table=table)
        print(sql_drop)
        conn.execute(sql_drop)
        conn.commit()
        conn.close()
        print('删除完成:', table)
        return True

    # 插入新的班级表
    def create_new_pc_table(self, profession, class_):
        table = profession + class_
        # 先检查是否存在相同名字的表
        sql = "SELECT COUNT(*) FROM sqlite_master where type='table' and name='{str}';".format(str=table)
        # print(sql)
        conn = db.connect(self.New_DB_Path)
        cursor = conn.cursor()
        conn.row_factory = db.Row
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows[0][0] == 1:
            print('存在相同名字的表')
            return False
        # 插入新表
        sql_createnewtable = 'CREATE TABLE {tablename}(' \
                             'lable varchar(10) not null,' \
                             ' name varchar(10) not null,' \
                             'sex varchar(1) not null,' \
                             'id int primary key not null,' \
                             'profession varchar(50) not null,' \
                             'features int,' \
                             'flag int default 0 not null' \
                             ');'.format(tablename=table)
        conn.execute(sql_createnewtable)
        conn.commit()
        conn.close()
        print('创建完成')
        return True

    # 查询所有表名
    def select_all_table(self):

        conn = db.connect(self.New_DB_Path)
        cursor = conn.cursor()
        conn.row_factory = db.Row

        # 查询所有表名
        sql_all_table = 'SELECT name FROM sqlite_master WHERE type="table" ORDER BY name;'
        # 查询表个数
        sql_all_num = 'select count(*) from sqlite_master where type="table"; '

        cursor.execute(sql_all_num)
        rows = cursor.fetchall()
        table_nmu = rows[0][0]
        print('总共有{num}个表'.format(num=table_nmu))

        cursor.execute(sql_all_table)
        rows = cursor.fetchall()
        print(rows)
        table_name = []
        for i in range(table_nmu):
            table_name.append(rows[i][0])

        return table_name, table_nmu

    # 插入新成员信息
    def insert_new_student(self, student_info):
        conn = db.connect(self.New_DB_Path)

        # 检测学号是否唯一
        sql_checkid = 'select COUNT(*) from {proclass} where id="{id}";'\
            .format(proclass=student_info[4], id=student_info[3])
        print(sql_checkid)

        cursor = conn.cursor()
        conn.row_factory = db.Row
        cursor.execute(sql_checkid)
        rows = cursor.fetchall()

        if rows[0][0] == 1:
            print('存在这个学号')
            return False
        print('新的个人数据')
        sql_insert = 'INSERT INTO {proclass} (lable,name,sex,id,profession) VALUES ' \
                     '("{lable}","{name}", "{sex}","{id}","{profession}");' \
            .format(proclass=student_info[4],
                    lable=student_info[0],
                    name=student_info[1],
                    sex=student_info[2],
                    id=student_info[3],
                    profession=student_info[4])
        print(sql_insert)
        conn.execute(sql_insert)
        conn.commit()
        conn.close()
        return True


if __name__ == "__main__":
    sql = Operate_Sql()
    sql.create_new_pc_table('CS', '172')
    # sql.delete_pc_table('CS', '172')
    sql.select_all_table()
