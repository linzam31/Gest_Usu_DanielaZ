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
        if rol == rol:
            
            if rol == "administrador":
                    return redirect(url_for("inicio"))
            else:
                    return "Bienvenido Empleado"
        else:
            return "Rol Incorrecto"

    else: 
        flash("Usuario o contraseña incorrecta", "danger")
        return redirect(url_for('login_form'))
# validar sesion en pag. inicial


@apps.route('/inicio')
def inicio():
    if  'usuario' not in session:
        return redirect(url_for('login'))
    
    con = conectar()
    cursor = con.cursor()
    
    cursor.execute("SELECT * FROM usuarios")
    u = cursor.fetchall()

    cursor.execute("SELECT * FROM empleado")
    empleado = cursor.fetchall()
    
    cursor.execute("SELECT * FROM departamento")
    departamento = cursor.fetchall()
    
    cursor.close()
    con.close()

    return render_template('index.html', user = u, emple = empleado, depa = departamento)

   
        
#cerrar la sesion
@apps.route('/salir')
def salir():
    session.clear()
    return redirect(url_for('login'))

@apps.route('/eliminar/<int:id>')
def eliminar_usuario(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    con= conectar()
    cursor = con.cursor()
    sql = "SELECT rol FROM usuarios WHERE id_usuario = %s"
    cursor.execute(sql, (id,))
   
    usuario = cursor.fetchone()
   
    if usuario:
        rol = usuario[0]
        if rol == "administrador":
            flash("No se puede eliminar el administrador")
        else:
            cursor.execute("DELETE  FROM usuarios WHERE id_usuario = %s", (id,))
            con.commit()
            flash("empleado eliminado")
    cursor.close()
    con.close()
    return redirect(url_for('inicio'))

@apps.route('/guardar_usuario', methods=['POST'])
def guardar_usuario():
    
    usuario = request.form['txtnombre']
    password = request.form['txtpass']
    rolusu = request.form['txtrol']
    documento = request.form['txtdocumento']
    
    #llamar a la conexión
    
    conn = conectar()
    cursor = conn.cursor()
    
    #crear el sql
    sql = "INSERT INTO usuarios (usuario, pasword, rol, docu_emple) VALUES (%s,%s,%s,%s) "
    cursor.execute(sql,(usuario, password, rolusu, documento))
    conn.commit()
    
    
    return redirect(url_for('inicio'))
sql = "SELECT docu_emple FROM usuarios where docu_emple = %s"


@apps.route('/registrar_empleado' , methods=['POST'])
def registrar_empleado():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    nombres = request.form['nombre']
    apellidos = request.form['apellido']
    departamento = request.form['departamento']  
    doc_emplea = request.form['documento']
    cargo = request.form['cargo'] 
    bonificacion = float(request.form['bonificacion'])
    ho_ex = int(request.form['ho_ex'])
    con = conectar()
    cursor = con.cursor()

    def salariob():
        if cargo == "gerente":
            return 5000000
        elif cargo == "administrador":
            return 3500000
        elif cargo == "contador":
            return 2800000
        else:
            return 1800000
    
    salariob = salariob()
    valorHExtra = ho_ex * 3000
    salariobru = salariob + valorHExtra + bonificacion
    salud = salariobru * 0.04
    pension = salariobru * 0.04
    salarioneto = salariobru - salud - pension
        
    con = conectar()
    cursor = con.cursor()
    sqldepa = "SELECT id_area FROM departamento WHERE nom_area = %s"
    cursor.execute(sqldepa, (departamento,))
    resultado = cursor.fetchone()
    if resultado:
        departamento = resultado[0]
    
        sql = "INSERT INTO empleado (nom_empleado,ape_empleado,documento, cargo, salario, horas_ex, bonificaciones, salud, pension, salarios_neto, id_dep) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        datos = ( nombres,apellidos,doc_emplea,cargo,salariobru, ho_ex, bonificacion,salud,pension,salarioneto, departamento)
        cursor.execute(sql, datos)
        con.commit()
        print("Empleado guardado en la base de datos")
    else:
        print("El departamento no existe, por favor registre el departamento antes de registrar el empleado")
    return redirect(url_for("inicio"))


@apps.route('/eliminar_empleado/<int:id>')
def eliminar_empleado(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    con= conectar()
    cursor = con.cursor()
    sql = "DELETE FROM empleado WHERE id_empleado = %s"
    cursor.execute(sql, (id,))
    con.commit()
    cursor.close()
    
    con.close()
    return redirect(url_for('inicio'))

#editar usuarios
@apps.route('/editar_usu/<int:id>')    
def editar_usu(id):

    
    if 'usuario' not in session:
        return redirect(url_for('login'))
    con = conectar()
    cursor = con.cursor()
    
    sql = "SELECT * FROM usuarios WHERE id_usuario = %s"
    cursor.execute(sql, (id,))
    usuario = cursor.fetchone()
    cursor.close()
    con.close()
    
    return render_template("editar_usu.html", usu = usuario)

@apps.route('/actualizar_usu/<int:id>', methods=['POST'])
def actualizar_usu(id):
    id = request.form['id']
    usuario = request.form['txtusuario']   
    password = request.form['txtpassword']

    con = conectar()
    cursor = con.cursor()
    
    sql = "UPDATE usuarios SET usuario = %s, pasword = %s WHERE id_usuario = %s"
    
    cursor.execute(sql, (usuario, password, id))
    con.commit()
    
    cursor.close()
    con.close()
    return redirect(url_for('inicio'))


@apps.route('/editar_empleado/<int:id>')
def editar_empleado(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    con = conectar()
    cursor = con.cursor()
    
    sql1 = "SELECT * FROM empleado WHERE id_empleado = %s"
    cursor.execute(sql1, (id,))
    empleado = cursor.fetchone()
    
    cursor.close()
    con.close()
    
    return render_template('editar_emple.html', emple=empleado)


@apps.route('/actualizar_emple/<int:id>', methods=['POST'])
def actualizar_emple(id):
    id = request.form['id']
    nombre = request.form['txtnombres']
    apellido = request.form['txtapellidos']
    cargo = request.form['txtcargo']
    horas_ex = int(request.form['txthoras_ex'])
    bonificacion = float(request.form['txtbonificacion'])
    departamento = request.form['txtdepartamento']
    
    def salariob():
        if cargo == "gerente":
            return 5000000
        elif cargo == "administrador":
            return 3500000
        elif cargo == "contador":
            return 2800000
        else:
            return 1800000
    
    salariob = salariob()
    valorHExtra = horas_ex * 3000
    salariobru = salariob + valorHExtra + bonificacion
    salud = salariobru * 0.04
    pension = salariobru * 0.04
    salarioneto = salariobru - salud - pension
        
    con = conectar()
    cursor = con.cursor()
    sqldepa = "SELECT id_area FROM departamento WHERE nom_area = %s"
    cursor.execute(sqldepa, (departamento,))
    resultado = cursor.fetchone()
    if resultado:
        departamento = resultado[0]
    
        sql = "UPDATE empleado SET nom_empleado = %s, ape_empleado = %s, cargo = %s, salario = %s, horas_ex = %s, bonificaciones = %s, salud = %s, pension = %s, salarios_neto = %s, id_dep = %s WHERE id_empleado = %s"
        
        datos = (nombre,apellido,cargo,salariobru,horas_ex,bonificacion,salud,pension,salarioneto, departamento, id)
        cursor.execute(sql, datos)
        con.commit()
 
        cursor.close()
        con.close()
    return redirect(url_for("inicio"))

    

if __name__ == '__main__':
    apps.run(debug=True)