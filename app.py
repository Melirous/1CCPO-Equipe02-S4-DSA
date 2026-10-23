"""Sprint 4 - Estação de Recarga. Backend Python (apenas biblioteca padrão).
Execute: python app.py  ->  http://localhost:8000
Fluxo: Interface (index.html) -> API HTTP (Handler) -> funções Python -> JSON -> Interface
"""
import json, os
from dataclasses import dataclass, asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

TARIFA_KWH = {"AC": 1.20, "DC": 2.10}   # R$ por kWh
TAXA_MINUTO = 0.05                       # R$ por minuto de ocupação


@dataclass
class Sessao:                            # estrutura de dados: 1 objeto = 1 sessão
    id: int
    veiculo: str
    energia: float                       # kWh
    tempo: int                           # minutos
    custo: float                         # R$
    carregador: str = "AC"
    data: str = "Nao informada"
    horario: str = "Nao informado"
    status: str = "Concluida"


sessoes = []                             # armazenamento: lista de objetos Sessao


def calcular_tarifa(energia, tempo, carregador):
    return round(energia * TARIFA_KWH[carregador] + tempo * TAXA_MINUTO, 2)


def busca_sequencial(lista, id_procurado):      # O(n)
    for i in range(len(lista)):
        if lista[i].id == id_procurado:
            return i
    return -1


def bubble_sort(lista, criterio):               # O(n²) no pior caso
    n = len(lista)
    for i in range(n):
        trocou = False
        for j in range(n - 1 - i):
            if getattr(lista[j], criterio) > getattr(lista[j + 1], criterio):
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                trocou = True
        if not trocou:                          # lista já ordenada: melhor caso O(n)
            break


def cadastrar(d):
    id_, carr = int(d["id"]), str(d.get("carregador", "AC")).upper()
    energia, tempo = float(d["energia"]), int(d["tempo"])
    if busca_sequencial(sessoes, id_) != -1:
        return False, "ID duplicado"
    if energia < 0 or tempo < 0 or carr not in TARIFA_KWH or not str(d["veiculo"]).strip():
        return False, "Dados inválidos"
    sessoes.append(Sessao(id_, str(d["veiculo"]).strip(), energia, tempo,
                          calcular_tarifa(energia, tempo, carr), carr,
                          d.get("data") or "Nao informada", d.get("horario") or "Nao informado"))
    return True, "Sessão cadastrada"


def estatisticas():
    if not sessoes:
        return {"total": 0, "energia": 0, "faturamento": 0, "ticket": 0, "maior": 0, "menor": 0}
    en = [s.energia for s in sessoes]
    fat = sum(s.custo for s in sessoes)
    return {"total": len(sessoes), "energia": round(sum(en), 2), "faturamento": round(fat, 2),
            "ticket": round(fat / len(sessoes), 2), "maior": max(en), "menor": min(en)}


def relatorio():
    e = estatisticas()
    linhas = ["===== RELATÓRIO FINAL =====",
              f"Sessões: {e['total']}", f"Energia total: {e['energia']:.2f} kWh",
              f"Faturamento: R$ {e['faturamento']:.2f}", f"Ticket médio: R$ {e['ticket']:.2f}"]
    for tipo in TARIFA_KWH:
        g = [s for s in sessoes if s.carregador == tipo]
        linhas.append(f"{tipo}: {len(g)} sessões, R$ {sum(s.custo for s in g):.2f}")
    return "\n".join(linhas)


def exemplo():
    for d in [(1, "BYD Dolphin", 32.5, 45, "AC"), (2, "Tesla Model 3", 57.3, 30, "DC"),
              (3, "Nissan Leaf", 8.7, 20, "AC"), (4, "Renault Zoe", 21.0, 60, "AC"),
              (5, "Volvo EX30", 45.9, 25, "DC")]:
        cadastrar(dict(zip(["id", "veiculo", "energia", "tempo", "carregador"], d)))


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, corpo, tipo="application/json"):
        dados = corpo if isinstance(corpo, bytes) else json.dumps(corpo, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", tipo + "; charset=utf-8")
        self.send_header("Content-Length", str(len(dados)))
        self.end_headers()
        self.wfile.write(dados)

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if u.path == "/":
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html"), "rb") as f:
                return self._send(200, f.read(), "text/html")
        if u.path == "/api/sessoes":                      # listagem (+ ordenação opcional)
            lista = list(sessoes)
            crit = q.get("ordenar", [""])[0]
            if crit in ("id", "energia", "custo", "tempo"):
                bubble_sort(lista, crit)
            return self._send(200, [asdict(s) for s in lista])
        if u.path == "/api/busca":
            try:
                i = busca_sequencial(sessoes, int(q.get("id", [""])[0]))
            except ValueError:
                return self._send(400, {"erro": "ID inválido"})
            return self._send(200 if i >= 0 else 404,
                              {"posicao": i, "sessao": asdict(sessoes[i])} if i >= 0 else {"erro": "Não encontrada"})
        if u.path == "/api/estatisticas":
            return self._send(200, estatisticas())
        if u.path == "/api/relatorio":
            return self._send(200, {"texto": relatorio()})
        self._send(404, {"erro": "Rota inexistente"})

    def do_POST(self):
        if self.path == "/api/exemplo":
            exemplo()
            return self._send(200, {"msg": "Dados de exemplo carregados"})
        if self.path == "/api/sessoes":
            try:
                corpo = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
                ok, msg = cadastrar(corpo)
            except (ValueError, KeyError):
                ok, msg = False, "Dados inválidos"
            return self._send(200 if ok else 400, {"msg": msg})
        self._send(404, {"erro": "Rota inexistente"})


if __name__ == "__main__":
    print("Servidor em http://localhost:8000")
    ThreadingHTTPServer(("", 8000), Handler).serve_forever()
