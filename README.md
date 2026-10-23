# Sprint 4 — Sistema de Gerenciamento de Estação de Recarga

Projeto da disciplina de **Data Structures & Algorithms (DSA)** — Turma **1CCPO**, Equipe 02.

## Integrantes

- João Victor Canello Ferian - RM573295
- Lucas Klein - RM570029
- Gustavo Melo dos Santos - RM573562
- João Pedro Costenari Silva - RM572260

## O problema

Uma estação de recarga de veículos elétricos precisa registrar cada sessão de recarga, calcular quanto cobrar, localizar sessões específicas, organizá-las por diferentes critérios e acompanhar números gerais (energia fornecida, faturamento etc.).

## Evolução do projeto

| Sprint | Entrega |
|--------|---------|
| 1 e 2 | _(preencher com o que foi feito)_ |
| 3 | Sistema em console (menu) com classe `Sessao`, busca sequencial e Bubble Sort |
| 4 | Mesmo núcleo em Python, agora com **interface web** + **API Flask**, **tarifação automática** e **relatório final** |

## Arquitetura

```
Interface Web (HTML/JS)  →  API Flask (app.py)  →  sessao.py (estruturas + algoritmos)
        ▲                                                       │
        └──────────────────── JSON ◄────────────────────────────┘
```

| Arquivo | Responsabilidade |
|---------|------------------|
| `backend/sessao.py` | Classe `Sessao`, lista de sessões, tarifação, busca, ordenação, estatísticas, relatório. **Python puro.** |
| `backend/app.py` | Rotas Flask: recebe JSON da interface, valida, chama `sessao.py` e devolve JSON. |
| `frontend/index.html` | Interface web: formulário, tabela, busca, ordenação, estatísticas e relatório. |

Toda a regra de negócio e todos os algoritmos estão em Python; o JavaScript apenas envia requisições e desenha os resultados.

## Como executar

```bash
pip install -r requirements.txt
cd backend
python app.py
```

Abra **http://localhost:5000** no navegador.

## Estrutura de dados

Cada sessão é um objeto da classe `Sessao`; as sessões ficam em uma **lista** (`sessoes = []`).

| Atributo | Descrição |
|----------|-----------|
| `id` | Identificador único |
| `veiculo` | Veículo recarregado |
| `energia` | Energia consumida (kWh) |
| `tempo` | Duração (minutos) |
| `carregador` | `AC` ou `DC` |
| `custo` | Calculado pelo backend (tarifação) |
| `data`, `horario`, `status` | Informações complementares |

**Por que classe + lista?** A classe agrupa todos os dados de uma sessão em um único objeto (`sessao.energia`, `sessao.custo`), e a lista permite guardar quantas sessões forem necessárias, percorrê-las em ordem e reordená-las no lugar.

## Tarifação

```
custo = energia × tarifa_do_carregador + tempo × R$ 0,05
```

| Carregador | Tarifa |
|------------|--------|
| AC | R$ 1,50 / kWh |
| DC (rápido) | R$ 2,40 / kWh |

Exemplo: 42,5 kWh em DC por 35 min → 42,5 × 2,40 + 35 × 0,05 = **R$ 103,75**.

## Algoritmos e complexidade

### Busca sequencial — O(n)

```python
def busca_sequencial(lista, id_procurado):
    for i in range(len(lista)):
        if lista[i].id == id_procurado:
            return i
    return -1
```

Chave: o `id`. Percorre da primeira à última sessão; termina ao encontrar o ID (retorna a posição) ou ao acabar a lista (retorna `-1`). No pior caso verifica as *n* sessões — 10 sessões, até 10 verificações; 1.000 sessões, até 1.000.

### Bubble Sort — O(n²)

```python
def bubble_sort(lista, criterio):
    n = len(lista)
    for i in range(n):
        trocou = False
        for j in range(n - 1 - i):
            if getattr(lista[j], criterio) > getattr(lista[j + 1], criterio):
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                trocou = True
        if not trocou:
            break
```

Campos de ordenação: `id`, `energia`, `custo` ou `tempo` (crescente). Compara vizinhos e troca quando o da esquerda é maior. Dois laços aninhados → **O(n²)** no pior caso; com a flag `trocou`, lista já ordenada custa **O(n)**.

### Resumo

| Operação | Complexidade | O que acontece quando as sessões aumentam |
|----------|--------------|--------------------------------------------|
| Cadastrar (`append`) | O(1) | Custo não muda |
| Verificar ID duplicado / buscar | O(n) | Dobrar as sessões dobra as verificações |
| Estatísticas e relatório | O(n) | Uma passada pela lista |
| Ordenar (Bubble Sort) | O(n²) | Dobrar as sessões ≈ quadruplica as comparações |

## API

| Método | Rota | Função |
|--------|------|--------|
| GET | `/api/sessoes` | Lista as sessões |
| POST | `/api/sessoes` | Cadastra uma sessão |
| GET | `/api/sessoes/<id>` | Busca por ID |
| POST | `/api/ordenar` | Ordena (`{"criterio": "energia"}`) |
| GET | `/api/estatisticas` | Estatísticas gerais |
| GET | `/api/relatorio` | Relatório final |
| GET | `/api/tarifa` | Calcula a tarifa (`?energia=&tempo=&carregador=`) |
| POST | `/api/exemplos` | Carrega dados de exemplo |
| POST | `/api/limpar` | Remove todas as sessões |

## Evoluções futuras

- Persistência em banco de dados (SQLite/PostgreSQL), para não perder sessões ao reiniciar.
- Tarifação dinâmica por horário de pico.
- Substituir o Bubble Sort por Merge Sort (O(n log n)) e indexar sessões em dicionário para busca O(1).
- Autenticação e histórico por usuário.
