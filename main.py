from flask import Flask, jsonify, render_template, request, redirect
import mysql.connector
import json
app = Flask(__name__)

@app.route('/', methods=['GET'])
def login():
    return render_template('login.html')
@app.route('/logar', methods=['POST'])
def logar():
    try:
        
        print("Dados recebidos:", request.form)
        email = request.form['email']
        senha = request.form['senha']
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="galaxvideo"
        )
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM Usuario WHERE Email = %s AND senha = %s"
        valores = (email, senha)
        cursor.execute(query, valores)
        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        if usuario:
            return jsonify({"autenticado": True, "usuarioId": usuario['idUser']}), 200
        else:
            return jsonify({"autenticado": False}), 401
    except Exception as e:
        print("Erro ao fazer login:", str(e))
        return jsonify({"erro": "Erro interno no Servidor"}, 500)
    
@app.route('/cadastrar', methods=['GET'])
def cadastro():
    return render_template('cadastro.html')

@app.route('/cadastro', methods=['POST'])
def cadastrar():
    try:
        print("Dados recebidos:", request.form)
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="galaxvideo"
        )
        print("Conexão bem-sucedida!")

        cursor = conn.cursor()

        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        sql = "INSERT INTO Usuario (Nome, Email, senha) VALUES (%s, %s, %s)"
        valores = (nome, email, senha)
        cursor.execute(sql, valores)
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"mensagem": "Você foi cadastrado com sucesso!"}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

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
@app.route('/buscar_filmes', methods=['GET'])
def buscar_filmes():
    termo_busca = request.args.get('q', '')  
    id_usuario = request.args.get('user_id', '')  

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="galaxvideo"
    )
    cursor = conn.cursor(dictionary=True)

    # 🔹 Adicionamos `usuario_id` na resposta para verificar o que está sendo processado
    cursor.execute("""
        SELECT f.idFilme, f.nomeFilme, f.imagem, f.Trailer, f.Categoria, f.AnoLanc, f.Sinopse, f.Classificação, f.NotaPublico AS nota,
               %s AS usuario_id,
               CASE WHEN EXISTS (
                   SELECT 1 FROM favoritos fav WHERE fav.filme_id = f.idFilme AND fav.usuario_id = %s
               ) THEN 1 ELSE 0 END AS isFavorito
        FROM filmes f
        WHERE f.nomeFilme LIKE %s
    """, (id_usuario, id_usuario, termo_busca + '%'))

    filmes = cursor.fetchall()
    conn.close()

    return app.response_class(
        response=json.dumps(filmes, ensure_ascii=False),
        status=200,
        mimetype='application/json; charset=utf-8'
    )
@app.route('/favoritar', methods=['POST'])
def favoritar_filme():
   
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="galaxvideo"
    )
    cursor = conn.cursor()

    data = request.json
    filme_id = data.get('filmeId')  # ID do filme recebido pelo frontend
    usuario_id = data.get('usuarioId')  # ID do usuário recebido pelo frontend

    cursor.execute("SELECT * FROM favoritos WHERE usuario_id = %s AND filme_id = %s", (usuario_id, filme_id))
    favorito = cursor.fetchone()

    if favorito:
        cursor.execute("DELETE FROM favoritos WHERE usuario_id = %s AND filme_id = %s", (usuario_id, filme_id))
        conn.commit()
        status = "removido"
    else:
        cursor.execute("INSERT INTO favoritos (usuario_id, filme_id) VALUES (%s, %s)", (usuario_id, filme_id))
        conn.commit()
        status = "adicionado"
    conn.close()
    return jsonify({"message": f"Filme {status} com sucesso!"})

@app.route('/meus-favoritos', methods=['POST'])
def meus_favoritos():

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="galaxvideo"
        )
        cursor = conn.cursor(dictionary=True)

        data = request.json
        usuario_id = data.get('usuarioId')  # ID do usuário recebido do frontend
        # Busca os filmes favoritados pelo usuário
        query = """
            SELECT filme_id 
            FROM favoritos 
            WHERE usuario_id = %s
        """
        cursor.execute(query, (usuario_id,))
        favoritos = cursor.fetchall()
        cursor.close()
        conn.close()
        # Retorna apenas os IDs dos filmes favoritados
        return jsonify([favorito['filme_id'] for favorito in favoritos]), 200
    except Exception as e:
        print("Erro ao buscar favoritos:", str(e))
        return jsonify({"erro": "Erro interno no Servidor"}), 500

@app.route('/favoritos-usuario', methods=['POST'])
def favoritos_usuario():

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="galaxvideo"
        )
        cursor = conn.cursor(dictionary=True)

        data = request.json
        usuario_id = data.get('usuarioId')

        # Retorna detalhes completos dos filmes favoritados
        query = """
            SELECT f.idFilme, f.nomeFilme, f.imagem, f.Trailer, f.Categoria, f.AnoLanc, 
                   f.Sinopse, f.Classificação, f.NotaPublico AS nota
            FROM favoritos fav
            INNER JOIN filmes f ON fav.filme_id = f.idFilme
            WHERE fav.usuario_id = %s
        """

        cursor.execute(query, (usuario_id,))
        filmes_favoritos = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(filmes_favoritos), 200
    except Exception as e:
        print("Erro ao buscar favoritos:", str(e))
        return jsonify({"erro": "Erro interno no Servidor"}), 500

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

@app.route('/filmes-por-genero', methods=['POST'])
def filmes_por_genero():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="galaxvideo"
        )
        cursor = conn.cursor(dictionary=True)

        data = request.json
        genero = data.get('genero')

        # Consulta SQL para buscar filmes pelo gênero escolhido
        query = """
            SELECT idFilme, nomeFilme, imagem, Categoria, AnoLanc, Classificação, NotaPublico AS nota
            FROM filmes
            WHERE Categoria LIKE %s
        """
        cursor.execute(query, (genero,))
        filmes_filtrados = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(filmes_filtrados), 200
    except Exception as e:
        print("Erro ao buscar filmes por gênero:", str(e))
        return jsonify({"erro": "Erro interno no Servidor"}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
