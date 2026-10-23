"""Estrutura de dados e algoritmos do sistema de recarga (Sprint 4).

Tudo que e regra de negocio, busca, ordenacao e estatistica esta aqui,
em Python puro, sem depender de Flask.
"""

# ---------------------------------------------------------------------------
# Tarifacao
# ---------------------------------------------------------------------------
TARIFA_KWH = {"AC": 1.50, "DC": 2.40}   # R$ por kWh, conforme o carregador
TAXA_MINUTO = 0.05                       # R$ por minuto de ocupacao da vaga


def calcular_tarifa(energia, tempo, carregador):
    """custo = energia * tarifa_do_carregador + tempo * taxa_por_minuto"""
    tarifa = TARIFA_KWH.get(carregador, TARIFA_KWH["AC"])
    return round(energia * tarifa + tempo * TAXA_MINUTO, 2)


# ---------------------------------------------------------------------------
# Estrutura de dados: cada sessao de recarga e um objeto Sessao
# ---------------------------------------------------------------------------
class Sessao:
    def __init__(self, id_sessao, veiculo, energia, tempo,
                 carregador="AC", data="Nao informada",
                 horario="Nao informado", status="Concluida", custo=None):
        self.id = id_sessao
        self.veiculo = veiculo
        self.energia = energia          # kWh
        self.tempo = tempo              # minutos
        self.carregador = carregador    # "AC" ou "DC"
        self.data = data
        self.horario = horario
        self.status = status
        # o custo e calculado pelo backend (tarifacao), nao digitado
        self.custo = custo if custo is not None else calcular_tarifa(
            energia, tempo, carregador)

    def to_dict(self):
        return {
            "id": self.id, "veiculo": self.veiculo, "energia": self.energia,
            "tempo": self.tempo, "custo": self.custo,
            "carregador": self.carregador, "data": self.data,
            "horario": self.horario, "status": self.status,
        }


# As sessoes ficam em uma lista (armazenamento em memoria)
sessoes = []


# ---------------------------------------------------------------------------
# Busca sequencial: O(n)
# ---------------------------------------------------------------------------
def busca_sequencial(lista, id_procurado):
    """Percorre a lista do inicio ao fim. Para ao achar o ID (retorna a
    posicao) ou ao terminar a lista sem achar (retorna -1)."""
    for i in range(len(lista)):
        if lista[i].id == id_procurado:
            return i
    return -1


# ---------------------------------------------------------------------------
# Bubble Sort: O(n^2) no pior caso, O(n) se a lista ja estiver ordenada
# ---------------------------------------------------------------------------
CRITERIOS = ("id", "energia", "custo", "tempo")


def bubble_sort(lista, criterio):
    """Ordena a lista in-place, em ordem crescente, pelo atributo `criterio`.
    Compara vizinhos e troca quando o da esquerda e maior que o da direita."""
    n = len(lista)
    for i in range(n):
        trocou = False
        for j in range(n - 1 - i):
            if getattr(lista[j], criterio) > getattr(lista[j + 1], criterio):
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                trocou = True
        if not trocou:      # nenhuma troca: ja esta ordenada
            break


# ---------------------------------------------------------------------------
# Estatisticas e relatorio: O(n) (uma passada pela lista)
# ---------------------------------------------------------------------------
def estatisticas(lista):
    if not lista:
        return {"total": 0, "energia_total": 0, "faturamento": 0,
                "ticket_medio": 0, "maior_consumo": 0, "menor_consumo": 0,
                "tempo_total": 0}
    energia_total = 0
    faturamento = 0
    tempo_total = 0
    maior = menor = lista[0].energia
    for s in lista:
        energia_total += s.energia
        faturamento += s.custo
        tempo_total += s.tempo
        if s.energia > maior:
            maior = s.energia
        if s.energia < menor:
            menor = s.energia
    return {
        "total": len(lista),
        "energia_total": round(energia_total, 2),
        "faturamento": round(faturamento, 2),
        "ticket_medio": round(faturamento / len(lista), 2),
        "maior_consumo": maior,
        "menor_consumo": menor,
        "tempo_total": tempo_total,
    }


def relatorio_final(lista):
    """Resumo final: estatisticas + quebra por tipo de carregador."""
    por_tipo = {}
    for s in lista:
        t = por_tipo.setdefault(s.carregador,
                                {"sessoes": 0, "energia": 0, "faturamento": 0})
        t["sessoes"] += 1
        t["energia"] = round(t["energia"] + s.energia, 2)
        t["faturamento"] = round(t["faturamento"] + s.custo, 2)
    return {"resumo": estatisticas(lista), "por_carregador": por_tipo}


# ---------------------------------------------------------------------------
# Dados de exemplo
# ---------------------------------------------------------------------------
def carregar_exemplos():
    base = [
        (1, "Tesla Model 3", 42.5, 35, "DC", "2026-10-20", "08:10"),
        (2, "BYD Dolphin", 28.0, 90, "AC", "2026-10-20", "09:45"),
        (3, "Nissan Leaf", 8.7, 25, "AC", "2026-10-21", "12:30"),
        (4, "Volvo EX30", 57.3, 40, "DC", "2026-10-21", "14:00"),
        (5, "Renault Kwid E-Tech", 12.4, 60, "AC", "2026-10-22", "18:20"),
    ]
    adicionadas = 0
    for id_, v, e, t, c, d, h in base:
        if busca_sequencial(sessoes, id_) == -1:
            sessoes.append(Sessao(id_, v, e, t, c, d, h))
            adicionadas += 1
    return adicionadas
