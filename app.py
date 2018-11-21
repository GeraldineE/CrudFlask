from flask import Flask, render_template, request, redirect, url_for,flash
from flask.ext.mysql import MySQL
import mysql.connector

app=Flask(__name__)
#config mysql conecction
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'flaskcontacts'

mysql=MySQL(app)
mysql.init_app(app)

app.secret_key = 'mysecretkey'

connection = mysql.connect()

@app.route('/')
def index():
    cur=connection.cursor()
    resultValue=cur.execute("SELECT * FROM contacts")
    if resultValue > 0:
        Details = cur.fetchall()
        return render_template('index.html', Details=Details)
    return  render_template('index.html')

@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        Details=request.form
        nombre=Details['nombre']
        apellido=Details['apellido']
        telefono=Details['telefono']
        email=Details['email']
        print(nombre)
        print(apellido)
        print(telefono)
        print(email)
        try:
            cur=connection.cursor()
            cur.execute("INSERT INTO contacts(nombre, apellido, telefono, email) VALUE(%s,%s,%s,%s)",(nombre,apellido,telefono,email))
            connection.commit()
            
        except Exception as e:
            print(str(e))
            #return redirect('/contacts')
    flash('Contacto fue agregado satisfactoriamente')
    return  redirect(url_for('index'))

@app.route('/contacts')
def contacts():
    cur=connection.cursor()
    resultValue=cur.execute("SELECT * FROM contacts")
    if resultValue > 0:
        Details = cur.fetchall()
        return render_template('contacts.html', Details=Details)
    
@app.route('/edit/<id>')
def edit(id):
    cur=connection.cursor()
    cur.execute("SELECT * FROM contacts WHERE id = %s",(id))
    Details = cur.fetchall()
    return render_template('edit.html', contact=Details[0])

@app.route('/update/<id>', methods = ['POST'])
def update(id):
    if request.method == 'POST':
        Details=request.form
        nombre=Details['nombre']
        apellido=Details['apellido']
        telefono=Details['telefono']
        email=Details['email']

        cur=connection.cursor()
        cur.execute(""" UPDATE contacts 
        SET nombre = %s,
        apellido = %s,
        telefono = %s,
        email = %s
        WHERE id = %s
        """, (nombre, apellido, telefono, email,id))
        connection.commit()
        flash('Contacto actualizado satisfactoriamente')
    return redirect(url_for('index'))


@app.route('/delete/<string:id>')
def delete(id):
    cur=connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    connection.commit()
    flash('contacto removido satisfactoriamente')
    return redirect(url_for('index'))


if __name__ == '__main__':
     app.run(debug=True)