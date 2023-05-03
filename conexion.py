import pymysql

def ObtenerConexion():
    return pymysql.connect(user='root', password='', host='localhost', port=3306,database='renta_casas')
    