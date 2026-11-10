import logging
from datetime import date, datetime
from pathlib import Path

import pymysql
import requests
from flask import Flask, jsonify, render_template, request

import database
from notificacoes import avisar_nova_ocorrencia
from validacao import validar_cadastro, validar_status

app = Flask(__name__)
app.json.ensure_ascii = False
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

# Guarda data, hora, ação e resultado em um arquivo local.
Path("logs").mkdir(exist_ok=True)
logging.basicConfig(filename="logs/acoes.log", level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s", encoding="utf-8")


def registrar(acao, resultado):
    logging.info("acao=%s resultado=%s", acao, resultado)


def resposta_erro(mensagem, codigo, acao):
    registrar(acao, f"erro_{codigo}")
    return jsonify({"erro": mensagem}), codigo


def formatar(registro):
    if not registro:
        return registro
    return {chave: valor.isoformat() if isinstance(valor, (date, datetime)) else valor
            for chave, valor in registro.items()}


@app.get("/")
def inicio():
    return render_template("index.html")


@app.get("/api/ocorrencias")
def listar():
    try:
        registros = [formatar(item) for item in database.listar_ocorrencias()]
        registrar("listar", "sucesso")
        return jsonify(registros), 200
    except pymysql.MySQLError:
        return resposta_erro("Não foi possível consultar as ocorrências.", 503, "listar")


@app.get("/api/ocorrencias/<int:identificador>")
def consultar(identificador):
    try:
        registro = database.buscar_ocorrencia(identificador)
        if not registro:
            return resposta_erro("Ocorrência não encontrada.", 404, "consultar")
        registrar("consultar", "sucesso")
        return jsonify(formatar(registro)), 200
    except pymysql.MySQLError:
        return resposta_erro("Não foi possível consultar a ocorrência.", 503, "consultar")


@app.post("/api/ocorrencias")
def cadastrar():
    dados, erro = validar_cadastro(request.get_json(silent=True))
    if erro:
        return resposta_erro(erro, 400, "cadastrar")
    try:
        identificador = database.criar_ocorrencia(dados)
        avisar_nova_ocorrencia(identificador)
        registrar("cadastrar", "sucesso")
        return jsonify({"mensagem": "Ocorrência cadastrada.", "id": identificador}), 201
    except pymysql.MySQLError:
        return resposta_erro("Não foi possível cadastrar a ocorrência.", 503, "cadastrar")


@app.put("/api/ocorrencias/<int:identificador>")
def atualizar(identificador):
    dados, erro = validar_status(request.get_json(silent=True))
    if erro:
        return resposta_erro(erro, 400, "atualizar")
    try:
        if not database.atualizar_ocorrencia(identificador, dados):
            return resposta_erro("Ocorrência não encontrada.", 404, "atualizar")
        registrar("atualizar", "sucesso")
        return jsonify({"mensagem": "Status atualizado."}), 200
    except pymysql.MySQLError:
        return resposta_erro("Não foi possível atualizar a ocorrência.", 503, "atualizar")


@app.delete("/api/ocorrencias/<int:identificador>")
def excluir(identificador):
    try:
        if not database.excluir_ocorrencia(identificador):
            return resposta_erro("Ocorrência não encontrada.", 404, "excluir")
        registrar("excluir", "sucesso")
        return "", 204
    except pymysql.MySQLError:
        return resposta_erro("Não foi possível excluir a ocorrência.", 503, "excluir")


@app.get("/api/cep/<cep>")
def consultar_cep(cep):
    # Busca dados públicos do endereço usando requests e JSON.
    if len(cep) != 8 or not cep.isdigit():
        return resposta_erro("CEP inválido.", 400, "cep")
    try:
        resposta = requests.get(f"https://viacep.com.br/ws/{cep}/json/", timeout=5)
        resposta.raise_for_status()
        dados = resposta.json()
        if dados.get("erro"):
            return resposta_erro("CEP não encontrado.", 404, "cep")
        registrar("cep", "sucesso")
        return jsonify({campo: dados.get(campo, "") for campo in ("cep", "logradouro", "bairro", "localidade", "uf")}), 200
    except (requests.RequestException, ValueError):
        return resposta_erro("Consulta de CEP indisponível.", 502, "cep")


@app.errorhandler(413)
def tamanho_excedido(_erro):
    return resposta_erro("Dados enviados acima do limite.", 413, "requisicao")


@app.errorhandler(404)
def rota_inexistente(_erro):
    return jsonify({"erro": "Rota não encontrada."}), 404


@app.errorhandler(405)
def metodo_invalido(_erro):
    return jsonify({"erro": "Método não permitido."}), 405



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
