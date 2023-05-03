import csv
from passlib.hash import sha256_crypt
from Levenshtein import distance
from conexion import ObtenerConexion

def registrarusuario(nombre, apellidoPa,apellidoMa,correo,usuario,password,celular):
    conexion = ObtenerConexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO usuario(nombre, apellido_paterno, apellido_materno,usuario,correo, celular,contraseña,id_tipo) VALUES (%s, %s, %s,%s,%s,%s,%s,%s)",
                       (nombre, apellidoPa,apellidoMa,usuario,correo,int(celular),password,int(3)))
    conexion.commit()


def registrartrabajadores(nombre, apellidoPa,apellidoMa,correo,usuario,password,celular):
    conexion = ObtenerConexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO usuario(nombre, apellido_paterno, apellido_materno,usuario,correo, celular,contraseña,id_tipo) VALUES (%s, %s, %s,%s,%s,%s,%s,%s)",
                       (nombre, apellidoPa,apellidoMa,usuario,correo,int(celular),password,int(2)))
    conexion.commit()
  

def registrardepartamentos(direccion, precio,cp,detalles):
    conexion = ObtenerConexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO casa(direccion, precio,cp,detalles) VALUES (%s, %s, %s,%s)",
                       (direccion, int(precio),int(cp),detalles))
    conexion.commit()


def registrarrenta(id_casa, id_cliente,fecha_inicio,fecha_salida,total):
    conexion = ObtenerConexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO reservacion(id_casa, id_cliente,fecha_inicio,fecha_salida,total) VALUES (%s, %s, %s,%s,%s)",
                       (int(id_casa),int(id_cliente),fecha_inicio,fecha_salida,int(total)))
    conexion.commit()


def obtener_depa_por_id(id):
    conexion = ObtenerConexion()
    depa = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, direccion, precio, cp, detalles FROM casa WHERE id = %s", (id,))
        depa = cursor.fetchone()
    conexion.close()
    return depa


def lee_diccionario_rentas_mysql()->list:
    diccionario = {}
    conexion = ObtenerConexion()
    with conexion.cursor() as cursor:
        query = "Select * from reservacion"
        
        cursor.execute(query)
        record = cursor.fetchall()
        #print (cursor.rowcount)
        for row in record:
            #print(row)
            llave = row[1]
            diccionario[llave]=row
        print (diccionario)
        return diccionario


def actualizar_depat(direccion, precio,cp,detalles, id):
    conexion = ObtenerConexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE casa SET direccion = %s, precio = %s, cp = %s, detalles = %s WHERE id = %s",
                       (direccion, int(precio),int(cp),detalles, id))
    conexion.commit()
    conexion.close()


def registrardiccionario()->list:
    return lee_diccionario_mysql()


def lee_diccionario_casa_mysql()->list:
    diccionario = {}
    conexion = ObtenerConexion()
    with conexion.cursor() as cursor:
        query = "Select * from casa"
        
        cursor.execute(query)
        record = cursor.fetchall()
        #print (cursor.rowcount)
        for row in record:
            #print(row)
            llave = row[0]
            diccionario[llave]=row
        return diccionario


def lee_diccionario_mysql()->list:
    diccionario = {}
    conexion = ObtenerConexion()
    with conexion.cursor() as cursor:
        query = "Select * from usuario"
        
        cursor.execute(query)
        record = cursor.fetchall()
        for row in record:
            llave = row[4]
            diccionario[llave]=row
            
        print (diccionario)
        return diccionario


def Busquedausuarios(usuario)->str:
    conexion = ObtenerConexion()
    with conexion.cursor() as cursor:
        query="""Select * from usuario where usuario = %s"""
        cursor.execute(query,(usuario))
        record = cursor.fetchall()

        for row in record:
            print("usuario = ", row[4], )
            login=row[4]
        return login
    
            