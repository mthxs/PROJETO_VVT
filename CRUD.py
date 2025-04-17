
import mysql.connector


def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="projetogit"
)

def listar_filmes():
    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT nomeFilme AS titulo,imagem, Sinopse as sinopse, NotaPublico AS nota FROM filmes")
    filmes = cursor.fetchall()
    conn.close()
    return filmes
