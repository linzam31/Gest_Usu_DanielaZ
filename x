@apps.route('/inicio_empleado')
def inicio_empleado():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    con = conectar()
    cursor = con.cursor()
    
    sql1 = "SELECT * FROM empleado"
    cursor.execute(sql1)
    empleado = cursor.fetchone()
    
    cursor.close()
    con.close()
    
    return render_template('panelempleado.html', emple=empleado)

nombre apellido cargo y departamento 
