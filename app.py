
from passlib.hash import sha256_crypt
from flask import Flask, render_template, request, redirect, session, url_for

from funciones import  lee_diccionario_rentas_mysql,registrarrenta,actualizar_depat,obtener_depa_por_id,registrartrabajadores,lee_diccionario_casa_mysql, registrardepartamentos, lee_diccionario_mysql,Busquedausuarios,registrarusuario
import datetime
from datetime import timedelta
#from flask_weasyprint import render_pdf



diccionario_users = lee_diccionario_mysql()
login_prueba=Busquedausuarios
diccionario_casas = lee_diccionario_casa_mysql()






logeado = False
first_login = False
deslog = False
confirmacion = False
invitado = False
id = 0


app = Flask(__name__)
app.secret_key = "klNmsS679SDqWpñl"

@app.route("/")
def index():
   
    if logeado == True:
        diccionario_casas = lee_diccionario_casa_mysql()
        user = session['usuario']
        print(diccionario_users[user][8])
        if diccionario_users[user][8] == 3:
                return render_template("index.html", first = first_login)
        else:
                if diccionario_users[user][8] == 2:
                    return render_template("index_admin.html", first = first_login)
    else:
        
        try:
            
            user = session['usuario']
            print(diccionario_users[user][8])
            if diccionario_users[user][8] == 3:
                return render_template("index.html", first = first_login)
            else:
                 if diccionario_users[user][8] == 2:
                    return render_template("index_admin.html", first = first_login)
        except:
            return render_template("index.html")


@app.route("/login/", methods=['GET','POST'])
def ingresar():
    diccionario_users = lee_diccionario_mysql()
    logeado = False
    if "logged_in" in session:
        if session["logged_in"] == True:
            logeado = True

    if logeado == False:        
        if request.method == 'GET':
            msg = ''
            return render_template('login.html',mensaje=msg)
        else:
            if request.method == 'POST':
                usuario = request.form['usuario']
                #print(diccionario_users)

                if usuario in diccionario_users:
                    password_db = diccionario_users[usuario][7] # password guardado
                    password_forma = request.form['password'] #password presentado
                    if password_db ==  password_forma:
                        session['usuario'] = usuario
                        session['logged_in'] = True
                        first_login = True
                        logeado = True
                        if diccionario_users[usuario][8] == 3:
                                return render_template("index.html", first = first_login)
                        else:
                            if diccionario_users[usuario][8] == 2:
                                return render_template("index_admin.html", first = first_login)

                    else:
                        msg = f'El password de {usuario} no corresponde'
                        print(msg)
                        return render_template('login.html',mensaje=msg)
                else:
                    msg = f'usuario {usuario} no existe'
                    return render_template('login.html',mensaje=msg)
    else:
        msg = 'YA ESTA LOGEADO'
        return render_template('index.html')
   

@app.route('/logout', methods=['GET'])
@app.route('/logout/', methods=['GET'])
def logout():
    if request.method == 'GET':
        session.clear()
        session["logged_in"] = False
        deslog = True
        logeado = False
        return render_template("index.html", deslogeado = deslog)



@app.route("/register/", methods=['POST','GET'])
def registrarse():
    if request.method == 'POST':
                valor = request.form['enviar']
                if valor == 'Entrar':
                    nombre  =  request.form['nombre']
                    apellidoPa  =  request.form['apellidoPaterno']
                    apellidoMa  =  request.form['apellidoMaterno']
                    correo    =  request.form['correo']
                    usuario =  request.form['usuario']
                    password = request.form['password']
                    celular = request.form['celular']
                    diccionario_users = lee_diccionario_mysql()
                    for row in diccionario_users:
                        if diccionario_users[row][4] == usuario:
                            return render_template("register.html")
                   
                    registrarusuario(nombre, apellidoPa,apellidoMa,correo,usuario,password,celular)
                   
                return redirect('/login')
    else:
     return render_template("register.html")


@app.route("/register_trabajadores/", methods=['POST','GET'])
def registrar_trabajadores():
    if request.method == 'POST':
                valor = request.form['enviar']
                if valor == 'Entrar':
                    nombre  =  request.form['nombre']
                    apellidoPa  =  request.form['apellidoPaterno']
                    apellidoMa  =  request.form['apellidoMaterno']
                    correo    =  request.form['correo']
                    usuario =  request.form['usuario']
                    password = request.form['password']   
                    celular = request.form['celular']
                    registrartrabajadores(nombre, apellidoPa,apellidoMa,correo,usuario,password,celular)             
                return render_template("/login.html")
    else:
     return render_template("register_trabajadores.html")


@app.route("/register_departamentos/", methods=['POST','GET'])
def registrar_departamentos():
    if request.method == 'POST':
                valor = request.form['enviar']
                if valor == 'Registrar':
                    direccion  =  request.form['direccion']
                    precio    =  request.form['precio']
                    cp =  request.form['cp']
                    detalles = request.form['detalles']
                    
                    print(direccion,precio,cp,detalles)
                    registrardepartamentos(direccion,precio,cp,detalles)
                    print(diccionario_casas)
                return render_template("index_admin.html")
    else:
     return render_template("register_departamentos.html")


@app.route("/rentar/<int:id>", methods=['POST','GET'])
def rentar_departamento(id):
    if request.method == 'POST':
                valor = request.form['enviar']
                if valor == 'terminar proceso':
                    depa = obtener_depa_por_id(id)
                    user = session['usuario']
                    print(diccionario_users[user][8])
                    cliente = diccionario_users[user][0]
                    total = depa[2]
                    hoy_completo = datetime.datetime.today()
                    mes=hoy_completo+timedelta(days=30)
                    fecha_hoy  = datetime.datetime.strftime(hoy_completo,"%Y-%m-%d")
                    
                    fecha    =  request.form['fecha']            
                                        
                    registrarrenta(id,cliente,fecha_hoy,fecha,total)
                    
                return render_template("index.html")
    else:
        depa = obtener_depa_por_id(id)
        hoy_completo = datetime.datetime.today()
        mes=hoy_completo+timedelta(days=30)
        fecha_hoy  = datetime.datetime.strftime(hoy_completo,"%Y-%m-%d")
        fecha_mes  = datetime.datetime.strftime(mes,"%Y-%m-%d")

        return render_template("rentar.html", mes = fecha_mes, hoy = fecha_hoy, depa=depa)


@app.route("/departamento/<int:id>")
def mostrar_departamento(id):
    depa = obtener_depa_por_id(id)
    
    return render_template("departamento.html",depa=depa)


@app.route("/formulario_editar_depa/<int:id>")
def editar_depa(id):
    depa = obtener_depa_por_id(id)
    return render_template("editar_depa.html", depa=depa)


@app.route("/actualizar_depa", methods=["POST"])
def actualizar_depa():
    id = request.form["id"]
    direccion  =  request.form['direccion']
    precio    =  request.form['precio']
    cp =  request.form['cp']
    detalles = request.form['detalles']
    actualizar_depat(direccion, precio, cp, detalles, id)
    return render_template("ver_depa.html", diccionario_casas = lee_diccionario_casa_mysql())


@app.route("/invitado")
def paginainvitado():
    invitado = True
    return render_template("index.html", invitado = invitado)


@app.route("/lista_usuarios/", methods=['GET'])
def lista_users():
     if request.method == 'GET':
        diccionario_users = lee_diccionario_mysql()
        
        return render_template("lista_usuarios.html",dicc_usuario=diccionario_users)


@app.route("/lista_departamentos/", methods=['GET'])
def lista_departamentos():
     if request.method == 'GET':
        dicc_casas = lee_diccionario_casa_mysql()
        print(dicc_casas)
        
        return render_template("lista_departamentos.html",diccionario_casas=dicc_casas)


@app.route("/ver_departamentos/", methods=['GET'])
def ver_departamentos():
     if request.method == 'GET':
        dicc_casas = lee_diccionario_casa_mysql()
    
        return render_template("ver_depa.html",diccionario_casas=dicc_casas)


@app.route("/lista_rentas/", methods=['GET'])
def lista_rentas():
     if request.method == 'GET':
        user = session['usuario']
        usuario = diccionario_users[user][0]
        print(diccionario_users[user][0])
        diccionario_rentas = lee_diccionario_rentas_mysql()
        
        return render_template("lista_rentas.html",dicc_rentas=diccionario_rentas,id=usuario)


@app.route("/busc_casas/", methods=['GET'])
def lista_casas():
    if request.method == 'GET':
        dicc_casas = lee_diccionario_casa_mysql()
        print(dicc_casas)
        return render_template("lista_casa.html",diccionario_casas=dicc_casas)


@app.route("/busc_casas_inv/", methods=['GET'])
def lista_casas_inv():
    if request.method == 'GET':
        dicc_casas = lee_diccionario_casa_mysql()
        print(dicc_casas)
        return render_template("inv_lista_casa.html",diccionario_casas=dicc_casas)


@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")       



if __name__ == "__main__":
    app.run(debug=True)
    session['logged_in'] = False