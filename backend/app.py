"""API Flask: camada fina que liga a interface web ao codigo Python.

Fluxo: Interface (fetch/JSON) -> rota Flask -> funcoes de sessao.py
       -> resultado em JSON -> Interface
"""
import os
from flask import Flask, jsonify, request, send_from_directory

import sessao as core

FRONTEND = os.path.join(os.path.dirname(__file__), "..", "frontend")
app = Flask(__name__, static_folder=None)


def erro(msg, codigo=400):
    return jsonify({"erro": msg}), codigo


def numero(valor, nome):
    try:
        n = float(valor)
    except (TypeError, ValueError):
        raise ValueError(f"{nome} invalido")
    if n < 0:
        raise ValueError(f"{nome} nao pode ser negativo")
    return n


@app.get("/")
def index():
    return send_from_directory(FRONTEND, "index.html")


@app.get("/api/sessoes")
def listar():
    return jsonify([s.to_dict() for s in core.sessoes])


@app.post("/api/sessoes")
def cadastrar():
    d = request.get_json(silent=True) or {}
    try:
        id_sessao = int(d.get("id"))
        if id_sessao <= 0:
            raise ValueError
    except (TypeError, ValueError):
        return erro("ID invalido (use um inteiro positivo)")
    if core.busca_sequencial(core.sessoes, id_sessao) != -1:
        return erro(f"Ja existe uma sessao com ID {id_sessao}", 409)
    veiculo = (d.get("veiculo") or "").strip()
    if not veiculo:
        return erro("Informe o veiculo")
    carregador = d.get("carregador", "AC")
    if carregador not in core.TARIFA_KWH:
        return erro("Carregador deve ser AC ou DC")
    try:
        energia = numero(d.get("energia"), "Energia")
        tempo = numero(d.get("tempo"), "Tempo")
    except ValueError as e:
        return erro(str(e))
    nova = core.Sessao(id_sessao, veiculo, energia, tempo, carregador,
                       d.get("data") or "Nao informada",
                       d.get("horario") or "Nao informado")
    core.sessoes.append(nova)
    return jsonify(nova.to_dict()), 201


@app.get("/api/sessoes/<int:id_sessao>")
def buscar(id_sessao):
    pos = core.busca_sequencial(core.sessoes, id_sessao)
    if pos == -1:
        return erro("Sessao nao encontrada", 404)
    return jsonify({"posicao": pos, "sessao": core.sessoes[pos].to_dict()})


@app.post("/api/ordenar")
def ordenar():
    criterio = (request.get_json(silent=True) or {}).get("criterio")
    if criterio not in core.CRITERIOS:
        return erro("Criterio deve ser: " + ", ".join(core.CRITERIOS))
    core.bubble_sort(core.sessoes, criterio)
    return jsonify([s.to_dict() for s in core.sessoes])


@app.get("/api/estatisticas")
def estatisticas():
    return jsonify(core.estatisticas(core.sessoes))


@app.get("/api/relatorio")
def relatorio():
    return jsonify(core.relatorio_final(core.sessoes))


@app.get("/api/tarifa")
def tarifa():
    try:
        energia = numero(request.args.get("energia"), "Energia")
        tempo = numero(request.args.get("tempo"), "Tempo")
    except ValueError as e:
        return erro(str(e))
    carregador = request.args.get("carregador", "AC")
    if carregador not in core.TARIFA_KWH:
        return erro("Carregador deve ser AC ou DC")
    return jsonify({"custo": core.calcular_tarifa(energia, tempo, carregador)})


@app.post("/api/exemplos")
def exemplos():
    n = core.carregar_exemplos()
    return jsonify({"adicionadas": n, "total": len(core.sessoes)})


@app.post("/api/limpar")
def limpar():
    core.sessoes.clear()
    return jsonify({"total": 0})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
