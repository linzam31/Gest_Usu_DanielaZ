from flask import Flask,render_template,request
from database import conectar
#crear app del proyecto

app = Flask(__name__)


#crear la ruta principal

@app.route('/')
def inicio():
    return render_template("index.html")

#crear la ruta para registrar usuarios



if __name__ == '__main__':
    app.run(debug=True)