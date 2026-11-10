import pymysql
from config import DB_CONFIG


def conectar():
    #abre uma conexão nova para cada operação.
    return pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)


def listar_ocorrencias():
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("SELECT id, titulo, descricao, categoria, cep, rua, bairro, cidade, uf, status, criado_em FROM ocorrencias ORDER BY id DESC LIMIT 100")
            return cursor.fetchall()


def buscar_ocorrencia(identificador):
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("SELECT id, titulo, descricao, categoria, cep, rua, bairro, cidade, uf, status, criado_em FROM ocorrencias WHERE id = %s", (identificador,))
            return cursor.fetchone()


def criar_ocorrencia(dados):
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("""INSERT INTO ocorrencias (titulo, descricao, categoria, cep, rua, bairro, cidade, uf, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (dados["titulo"], dados["descricao"], dados["categoria"], dados["cep"],
                 dados["rua"], dados["bairro"], dados["cidade"], dados["uf"], "aberta"))
            novo_id = cursor.lastrowid
        conexao.commit()
        return novo_id


def atualizar_ocorrencia(identificador, dados):
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("UPDATE ocorrencias SET status = %s WHERE id = %s", (dados["status"], identificador))
            alteradas = cursor.rowcount
        conexao.commit()
        return alteradas > 0


def excluir_ocorrencia(identificador):
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("DELETE FROM ocorrencias WHERE id = %s", (identificador,))
            alteradas = cursor.rowcount
        conexao.commit()
        return alteradas > 0
