from flask import Flask, jsonify, render_template, request
import mysql.connector
import json
app = Flask(__name__)

@app.route('/')
def login():
    return render_template('')
@app.route('/menu')
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
    cursor.execute("SELECT idFilme, nomeFilme, imagem, Trailer, Categoria, AnoLanc, Sinopse,Classificação, NotaPublico AS nota FROM filmes")
    filmes = cursor.fetchall()
    conn.close()
    
    return app.response_class(
        response=json.dumps(filmes, ensure_ascii=False),  # 🔹 Mantém acentos corretamente
        status=200,
        mimetype='application/json; charset=utf-8'
    )
@app.route('/favoritar', methods=['POST'])
def favoritar_filme():
    data = request.json
    filme_id = data.get('id')
@app.route('/cadastrarfilme',methods=['GET'])
def cadastrofilme():
    return render_template('cadastrarfilme.html')

@app.route('/cadastrofilme', methods=['POST'])
def cadastrar_filme():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="galaxvideo"
        )
        print("Conexão bem-sucedida!")

        cursor = conn.cursor()

        nome = request.form['nome']
        ano = request.form['ano']
        categoria = request.form['categoria']
        classificacao = request.form['classificacao']
        sinopse = request.form['sinopse']
        nota = request.form['nota']
        imagem = request.form['imagem']
        trailer = request.form['trailer']

        # Inserindo no banco de dados
        sql = "INSERT INTO filmes (nomeFilme, AnoLanc, Categoria, imagem, Trailer, Classificação, Sinopse, NotaPublico) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        valores = (nome, ano, categoria, imagem, trailer, classificacao, sinopse, nota)
        cursor.execute(sql, valores)
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"mensagem": "Filme cadastrado com sucesso!"}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)
