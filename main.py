from flask import Flask, jsonify, render_template, request, redirect, session
import mysql.connector
import json
import random
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
app = Flask(__name__)
app.secret_key = 'MFDAI33312D12332'
def conneector_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="galaxvideo"
    )
def enviar_email_codigo(destinatario, codigo):
    remetente = "galaxvideostreming@gmail.com"
    senha = "cxiq zxog dswo huai"  # Use senha de app do Gmail
    msg = MIMEText(f"Seu código de recuperação é: {codigo}")
    msg['Subject'] = "Recuperação de senha - Galax Video"
    msg['From'] = remetente
    msg['To'] = destinatario

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(remetente, senha)
        smtp.send_message(msg)

@app.route('/', methods=['GET'])
def login():
    return render_template('login.html')
@app.route('/logar', methods=['POST'])
def logar():
    try:
        email = request.form['email']
        senha = request.form['senha']
        conn = conneector_banco() 
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM Usuario WHERE Email = %s AND senha = %s"
        valores = (email, senha)
        cursor.execute(query, valores)
        usuario = cursor.fetchone()

        is_admin = False
        if usuario:
            cursor.execute("SELECT 1 FROM admin WHERE usuario_id = %s", (usuario['idUser'],))
            is_admin = cursor.fetchone() is not None

        cursor.close()
        conn.close()
        
        if usuario:
            return jsonify({"autenticado": True, "usuarioId": usuario['idUser'], "isAdmin": is_admin}), 200
        else:
            return jsonify({"autenticado": False}), 401

    except Exception as e:
        print("Erro ao fazer login:", str(e)) 
        return jsonify({"erro": "Erro interno no Servidor", "detalhes": str(e)}), 500  
@app.route('/cadastrar', methods=['GET'])
def cadastro():
    return render_template('cadastro.html')
@app.route('/cadastro', methods=['POST'])
def cadastrar():
    try:
        print("Dados recebidos:", request.form)
        conn = conneector_banco() 
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

@app.route('/recuperar_senha', methods=['GET'])
def recuperar_senha():
    return render_template('recuperarsenha.html')
@app.route('/recuperar-senha', methods=['POST'])
def enviar_codrec():
    data = request.get_json()
    email = data.get('email')
    conn = conneector_banco()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT idUser FROM usuario WHERE Email = %s", (email,))
    usuario = cursor.fetchone()
    if not usuario:
        return jsonify({"sucesso": False}), 200
    
    codigo = str(random.randint(100000, 999999))
    timenow = datetime.now()
    cursor.execute(
        "INSERT INTO recuperacao_senha (usuario_id, codigo, criado_em) VALUES (%s, %s, %s)",
        (usuario['idUser'], codigo, timenow)
    )
    conn.commit()
    cursor.close()
    conn.close()

    enviar_email_codigo(email, codigo)
    
    return jsonify({"sucesso": True}), 200
@app.route('/verificar-codigo', methods=['POST'])
def verificar_codigo():
    data = request.get_json()
    codigo = data.get('codigo')
    conn = conneector_banco()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT usuario_id FROM recuperacao_senha
        WHERE codigo = %s AND criado_em >= (NOW() - INTERVAL 15 MINUTE)
        ORDER BY criado_em DESC LIMIT 1
    """, (codigo,))
    registro = cursor.fetchone()
    cursor.close()
    conn.close()
    if registro:
        session['recupera_usuario_id'] = registro['usuario_id']
        return jsonify({"sucesso": True})
    else:
        return jsonify({"sucesso": False, "erro": "Código inválido ou expirado."})
@app.route('/nova-senha', methods=['POST'])
def nova_senha():
    data = request.get_json()
    senha = data.get('senha')
    usuario_id = session.get('recupera_usuario_id')
    if not usuario_id:
        return jsonify({"sucesso": False, "erro": "Sessão expirada. Tente novamente."})
    conn = conneector_banco()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuario SET senha = %s WHERE idUser = %s", (senha, usuario_id))
    conn.commit()
    cursor.close()
    conn.close()
    session.pop('recupera_usuario_id', None)
    return jsonify({"sucesso": True})
@app.route('/menu')
def index():
    
    return render_template('index.html')

@app.route('/filmes', methods=['GET'])
def listar_filmes():
    
    conn = conneector_banco() 
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT idFilme, nomeFilme, imagem, Trailer, Categoria, AnoLanc, Sinopse,Classificação, NotaPublico AS nota FROM filmes")
    filmes = cursor.fetchall()
    conn.close()
    
    return app.response_class(
        response=json.dumps(filmes, ensure_ascii=False),  # 🔹 Mantém acentos corretamente
        status=200,
        mimetype='application/json; charset=utf-8'
    )
@app.route('/filme/<int:filmeId>', methods=['GET'])
def obter_filme(filmeId):
    try:
        conn = conneector_banco() 
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM Filmes WHERE idFilme = %s"
        cursor.execute(query, (filmeId,))
        filme = cursor.fetchone()

        cursor.close()
        conn.close()

        if filme:
            return jsonify(filme), 200
        else:
            return jsonify({"erro": "Filme não encontrado!"}), 404

    except Exception as e:
        print("❌ Erro ao obter filme:", str(e))
        return jsonify({"erro": "Erro interno no servidor"}), 500
@app.route('/buscar_filmes', methods=['GET'])
def buscar_filmes():
    termo_busca = request.args.get('q', '')  
    id_usuario = request.args.get('user_id', '')  

    conn = conneector_banco() 
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
   
    conn = conneector_banco() 
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
        conn = conneector_banco() 
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
        conn = conneector_banco() 
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
        conn = conneector_banco() 
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

@app.route('/deletarFilme/<int:filmeId>', methods=['DELETE'])
def deletar_filme(filmeId):
    try:
        print(f"ID recebido para exclusão: {filmeId}")
        conn = conneector_banco() 
        cursor = conn.cursor()
        
        query_favoritos = "DELETE FROM Favoritos WHERE filme_id = %s"
        cursor.execute(query_favoritos, (filmeId,))

        query = "DELETE FROM Filmes WHERE idFilme = %s"
        cursor.execute(query, (filmeId,))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"mensagem": "Filme deletado com sucesso!"}), 200

    except Exception as e:
        print("Erro ao deletar filme:", str(e))
        return jsonify({"erro": "Erro interno no servidor"}), 500
    
@app.route('/editarFilme/<int:filmeId>', methods=['PUT'])
def editar_filme(filmeId):
    try:
        print(f"ID recebido para edição: {filmeId}")
        dados = request.json  # 🔹 Obtém os dados enviados pelo frontend

        conn = conneector_banco() 
        cursor = conn.cursor()

        query = """
            UPDATE Filmes 
            SET nomeFilme = %s, AnoLanc = %s, Categoria = %s, Sinopse = %s 
            WHERE idFilme = %s
        """
        cursor.execute(query, (
            dados["nomeFilme"], dados["AnoLanc"], 
            dados["Categoria"], dados["Sinopse"], filmeId
        ))

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensagem": "Filme atualizado com sucesso!"}), 200
    except Exception as e:
        print("❌ Erro ao editar filme:", str(e))
        return jsonify({"erro": "Erro interno no servidor"}), 500    

@app.route('/filmes-por-genero', methods=['POST'])
def filmes_por_genero():
    try:
        conn = conneector_banco() 
        cursor = conn.cursor(dictionary=True)

        data = request.json
        genero = data.get('genero')
        id_usuario = data.get('user_id')  # Recebe o ID do usuário no JSON

        # Consulta SQL para buscar filmes pelo gênero e verificar se são favoritos
        query = """
            SELECT f.idFilme, f.nomeFilme, f.imagem, f.Categoria, f.AnoLanc, f.Classificação, f.NotaPublico AS nota,
                   CASE WHEN EXISTS (
                       SELECT 1 FROM favoritos fav WHERE fav.filme_id = f.idFilme AND fav.usuario_id = %s
                   ) THEN 1 ELSE 0 END AS isFavorito
            FROM filmes f
            WHERE f.Categoria LIKE %s
        """
        cursor.execute(query, (id_usuario, genero))
        filmes_filtrados = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(filmes_filtrados), 200
    except Exception as e:
        print("Erro ao buscar filmes por gênero:", str(e))
        return jsonify({"erro": "Erro interno no Servidor"}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
