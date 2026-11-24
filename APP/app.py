import os
import mysql.connector
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def health_check():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "db_mysql"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "root123"),
            database=os.getenv("DB_NAME", "poli_ci_db")
        )
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION();")
        version = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify({
            "estado": "OK",
            "mensaje": "Comunicacion exitosa entre contenedor Python y MySQL",
            "mysql_version": version[0]
        }), 200
    except Exception as e:
        return jsonify({"estado": "ERROR", "detalle": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)