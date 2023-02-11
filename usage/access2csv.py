import pypyodbc
import pandas
path = r'12.16-12.31.mdb'  # 数据库文件
table = '3310_20221216_20221231' # table name
savePath = r'12.16-12.31.csv'


def getAllColumnName(filePath, tableName):
    """
    输出表的字段名
    :param filePath: mdb文件路径
    :param tableName: mdb表名
    :return: 返回一个存储所有字段名的list
    """
    pypyodbc.lowercase = False  # 是否将字段名转为小写
    conn = pypyodbc.connect(
        r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + filePath + ";Uid=;Pwd=;")
    cursor = conn.cursor()
    sql = "SELECT TOP 1 * FROM " + tableName
    cursor.execute(sql)
    list = []
    for col in cursor.description:
        list.append(col[0])
    return list


def getAllRows(filePath, tableName):
    """
    返回遍历的所有行数据
    :param filePath: mdb文件路径
    :param tableName: mdb表名
    :return: 返回pypyodbc.Cursor类型
    """
    pypyodbc.lowercase = False  # 是否将字段名转为小写
    conn = pypyodbc.connect(
        r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + filePath + ";Uid=;Pwd=;")
    cursor = conn.cursor()
    sql = "SELECT * FROM " + tableName
    params = cursor.execute(sql)
    print(type(params))
    return params


def save2csv(columnName, list, savePath):
    """
    按照字段名columnName, 数据list存储在savePath路径上
    :param columnName:字段名
    :param list:数据
    :param savePath:csv存储路径
    """
    pandas.DataFrame(columns=columnName, data=list).to_csv(
        savePath, encoding="utf_8_sig", index=False)


columnName = getAllColumnName(path, table)
dataList = getAllRows(path, table)
save2csv(columnName, dataList, savePath)
print("done.")
