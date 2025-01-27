from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from dotenv import load_dotenv
import os
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

def get_db_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            port=int(os.getenv('DB_PORT', 29218))
        )
    except Exception as e:
        logging.error(f"Error de conexión a BD: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            email = request.form['email']
            mensaje = request.form['mensaje']
            
            conn = get_db_connection()
            if not conn:
                return "Error de conexión a la base de datos", 500
            
            cursor = conn.cursor()
            sql = "INSERT INTO registros (nombre, email, mensaje) VALUES (%s, %s, %s)"
            values = (nombre, email, mensaje)
            
            cursor.execute(sql, values)
            conn.commit()
            cursor.close()
            conn.close()
            
            return render_template('success.html')
        except Exception as e:
            logging.error(f"Error en submit: {e}")
            return "Error al procesar el formulario", 500

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    app.run(host='0.0.0.0', port=port) 