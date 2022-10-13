from crypt import methods
from urllib.request import Request
from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL

app = Flask(__name__)

#Conexion con la base de datos
mysql = MySQL
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sistema'
mysql.init_app(app)

@app.route('/')
def index():
    sql = "SELECT * FROM 'empleados';"
    conn = mysql.connect()
    cursor = conn.cursor() #Cursor almacena lo que se va a ejecutar
    cursor.execute(sql)
    empleados = cursor.fetchall()
    print(empleados)
    conn.commit() #Termina la conexión
    return render_template('empleados/index.html', empleados=empleados)

@app.route('/guardar')
def guardar():
    return render_template('empleados/guardar.html') 

@app.route('/store', methods=['POST'])
def storage():
    Cedula = request.form ['txt-input-ced']
    Nombre = request.form ['txt-input-nom']
    Dirección = request.form ['txt-input-direc']
    Correo = request.form ['txt-input-cor']
    Contraseña = request.form ['pwd']
    sql= "INSERT INTO 'empleados' ('Cedula', 'Nombre', 'Dirección', 'Correo', 'Contraseña') VALUES (NULL, %s, %s, %s, %s, %s);"
    
    datos = (Cedula, Nombre, Dirección, Correo, Contraseña)
    
    conn = mysql.connect()
    cursor = conn.cursor() #Cursor almacena lo que se va a ejecutar
    cursor.execute(sql, datos)
    conn.commit() #Termina la conexión
    return redirect('/')

#Código para eliminar
@app.route('/destroy/<int:Cedula>')
def destroy(Cedula):
    conn = mysql.connect()
    cursor = conn.cursor() #Cursor almacena lo que se va a ejecutar
    cursor.execute("DELETE FROM empleados WHERE Cedula=%s",(Cedula))
    conn.commit() #Termina la conexión
    return redirect('/')

#Editar
#Cargar el dato según cédula
@app.route('/edit/<int:Cedula>')
def editar(Cedula):
    conn = mysql.connect()
    cursor = conn.cursor() #Cursor almacena lo que se va a ejecutar
    cursor.execute("SELECT * FROM empleados WHERE id=%s",(Cedula))
    empleados=cursor.fetchall()
    conn.commit() #Termina la conexión
    return render_template('empleados/editar.html', empleados=empleados) 

#Editar dato seleccionado
@app.route('/update/', methods=['POST'])
def update():
    Cedula = request.form ['txt-input-ced']
    Nombre = request.form ['txt-input-nom']
    Dirección = request.form ['txt-input-direc']
    Correo = request.form ['txt-input-cor']
    Contraseña = request.form ['pwd']
    sql= "UPDATE empleados SET Nombre=%s, Dirección=%s, Correo=%s, Contraseña=%s WHERE Cedula=%s ;"
    datos = (Nombre, Dirección, Correo, Contraseña, Cedula)
    
    conn = mysql.connect()
    cursor = conn.cursor() #Cursor almacena lo que se va a ejecutar
    cursor.execute(sql, datos)
    conn.commit() #Termina la conexión
    return redirect('/')

if __name__== '__main__':
    app.run(debug=True)
.
