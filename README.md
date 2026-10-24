# Sprint 4 — Estação de Recarga (Demonstração e Defesa Técnica)

**Disciplina:** Data Structures and Algorithms (DSA) · **Turma:** 1CCPO · **Equipe 02**

## Integrantes
- João Victor Canello Ferian — RM573295
- Lucas Klein — RM570029
- Gustavo Melo dos Santos — RM573562
- João Pedro Costenari Silva — RM572260

## Como executar
```
python app.py        # Python 3.9+, sem dependências externas
```
Abra http://localhost:8000

## Link do vídeo:
https://youtu.be/e1v39awbE84

## Arquitetura
`Interface Web (index.html)` → `API HTTP (app.py)` → `Funções Python` → `JSON` → `Interface`

| Elemento | Implementação |
|---|---|
| Sessão | `@dataclass Sessao` (id, veículo, energia, tempo, custo, carregador, data, horário, status) |
| Armazenamento | `sessoes = []` (lista de objetos) |
| Tarifação | `calcular_tarifa`: kWh × tarifa (AC R$1,20 / DC R$2,10) + R$0,05 por minuto |
| Busca | `busca_sequencial` por ID — **O(n)** |
| Ordenação | `bubble_sort` por id/energia/custo/tempo — **O(n²)** pior caso, O(n) melhor caso |
| Estatísticas / relatório | `estatisticas()` e `relatorio()` — O(n) |
| Cadastro | O(n) (verifica ID duplicado com a busca sequencial) · `append` O(1) |

## Evolução
Sprint 3: menu em console (`Sessao`, Busca Sequencial, Bubble Sort).
Sprint 4: mesma lógica + tarifação, relatório e interface Web integrada ao backend.
