from flask import Flask,render_template,request
from database import conectar
#crear app del proyecto

app = Flask(__name__)


#crear la ruta principal

@app.route('/')
def inicio():
    return render_template("index.html")

#crear la ruta para registrar usuarios
@app.route('/guardar_usuario', methods=['POST'])
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
    
    
    return "Usuario guardado"


if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    
    
    
#validar que el empleado ya exista:       o no en la base de datos
# si no existe: no esta registrado el empleado