from flask import Flask, jsonify, render_template
import mysql.connector
import json
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/filmes', methods=['GET'])
def listar_filmes():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="galaxvideo"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT nomeFilme, imagem, Categoria, Sinopse AS sinopse, NotaPublico AS nota FROM filmes")
    filmes = cursor.fetchall()
    conn.close()
    
    return app.response_class(
        response=json.dumps(filmes, ensure_ascii=False),  # 🔹 Mantém acentos corretamente
        status=200,
        mimetype='application/json; charset=utf-8'
    )

@app.route('/cadastrofilme')
def cadastrofilme():
    return render_template('cadastrarfilme.html')

if __name__ == '__main__':
    app.run(debug=True)
