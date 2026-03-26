from flask import Flask, render_template,url_for,request,flash,redirect,session
from database import conectar


#crear la app del proyecto

apps = Flask(__name__)
apps.secret_key = "987654321"

@apps.route('/')
def login():
    return render_template("login.html")

#crear ruta de ingresar

@apps.route('/', methods=['POST'])
def login_form():
    
    
    #crea variables de python para recibir el formulario
    user = request.form['txtusu']
    password = request.form['txtcontra']
    
    #llamar a la base de datos
    con = conectar()
    cursor = con.cursor()
    
    sql = "SELECT * FROM usuarios WHERE usuario=%s AND pasword=%s"
    cursor.execute(sql,(user,password))
    
    user= cursor.fetchone()
    
    if user:
        
        #guardar las variables de sesion
        session['usuario'] = user[1]
        session['rol'] = user [3]
        
        rol = user [3]
        #if rol == rol:
            
        if user[3] == "administrador":
                return render_template("index.html")
        else:
                return "Bienvenido Empleado"
        #else:
            #return "Rol Incorrecto"
    
    else: 
        flash("Usuario o contraseña incorrecta", "danger")
        return redirect(url_for('login_form'))
# validar sesion en pag. inicial


@apps.route('/inicio')
def inicio():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    else:
        render_template('index.html')
        
#cerrar la sesion
@apps.route('/salir')
def salir():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    apps.run(debug=True)