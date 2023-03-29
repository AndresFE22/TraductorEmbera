from flask import Flask, render_template, request, redirect, url_for, flash, Response, make_response, jsonify
import mysql.connector
from mysql.connector import connect 
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from jinja2 import Template
import os
from functools import wraps
from datetime import datetime


app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Definir la función user_loader
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

#Conectar a base de datos
cnx = connect (
    host ="localhost",
    user ="root",
    password ="",
    database ="traductor"
)

if cnx.is_connected():
    print("Conexion a la base de datos establecida correctamente")

app.config['SECRET_KEY'] = 'clave-secreta'  # Cambia esto por una clave secreta fuerte



@app.route('/auth', methods=['POST'])
def auth():
    #Extracción de datos de usuario
    username = request.form['username']
    password = request.form['password']

    # Si el usuario y la contraseña son correctos, redirige a la página de inicio
    # De lo contrario, muestra un mensaje de error en la página de login
    if username == 'user' and password == 'clave':
        if current_user.is_authenticated:  # si el usuario ya ha iniciado sesión
            return redirect('/historial')
        else:  # si el usuario inicia sesión por primera vez
            user = User(id=1)  # crear un objeto de usuario
            login_user(user)  # iniciar sesión al usuario
            # Agregar encabezados de respuesta para evitar el almacenamiento en caché
            response = make_response(redirect('/historial'))
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '-1'
            return response
    else:
        return render_template('ingresar.html', error='Nombre de usuario o contraseña incorrectos')


#Ruta de inicio
@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        idiom1 = request.form['trd']
        idiom2 = request.form['trd2']
        varidioma = request.form['text1']             
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='traductor')
        cursor = conn.cursor()
        
        #Consulta en caso de valores iguales
        
        if idiom1 == '0' and idiom2 == '0':
            consulta = "SELECT español FROM palabras WHERE español = %s"
            palabra = (varidioma,)
            cursor.execute(consulta, palabra)
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            
            # Construir una cadena de texto amigable para el usuario final
            output = ''
            for palabra in data:
                output += palabra[0] + ' '
            
            return render_template('index.html', traduccion=output)
        
        elif idiom1 == '1' and idiom2 == '1':
            consulta = "SELECT embera FROM palabras WHERE embera = %s"
            palabra = (varidioma,)
            cursor.execute(consulta, palabra)
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            
            # Construir una cadena de texto amigable para el usuario final
            output = ''
            for palabra in data:
                output += palabra[0] + ' '
            
            return render_template('index.html', traduccion=output)
        
        #Consulta de diferentes idioma      
        
        elif idiom1 == '0' and idiom2 == '1':
            consulta = "SELECT embera FROM palabras WHERE español = %s"
            palabra = (varidioma,)
            cursor.execute(consulta, palabra)     
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            
            # Construir una cadena de texto amigable para el usuario final
            output = ''
            for palabra in data:
                output += palabra[0] + ' '
                
            return render_template('index.html', traduccion=output)
        
        elif idiom1 == '1' and idiom2 == '0':
            consulta = "SELECT español FROM palabras WHERE embera = %s"
            palabra = (varidioma,)
            cursor.execute(consulta, palabra)     
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            
            # Construir una cadena de texto amigable para el usuario final
            output = ''
            for palabra in data:
                output += palabra[0] + ' '
                
            return render_template('index.html', traduccion=output)
            
    else:
        return render_template('index.html', traduccion="")

        




#Ruta de introducir palabras

@app.route('/historial', methods=['GET', 'POST'])
@login_required
def introducir():
    
    if request.method == 'POST':

        español = request.form['español']
        embera = request.form['embera']
       # resultado = "Texto traducido" # Aquí debería estar el resultado de la traducción
    
        # Conexión a la base de datos y creación del cursor
        cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='traductor')
        cursor = cnx.cursor()

        # Creación de la consulta para insertar la traducción en la base de datos
        query = "INSERT INTO palabras (español, embera) VALUES (%s, %s)"
        data = (español, embera)

        # Ejecución de la consulta y commit de la transacción
        cursor.execute(query, data)
        cnx.commit()

        # Cierre del cursor y la conexión
        cursor.close()
        cnx.close()
        
        #Mostrar mensaje de éxito 
        
        msge = f"{español}' y '{embera}' guardadas correctamente"
        
        
        return render_template('historial.html', showModal=True, msge=msge)
    else:
        return render_template('historial.html', showModal=False )
    






if __name__ == '__main__':
    app.run(debug=True)
