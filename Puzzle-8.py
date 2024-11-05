# Import de time - fará o cálculo do tempo dos algoritmos para a resolução do puzzle
import time
# Importe de heapq - fila de prioridade que sempre mantém o menor elemento no topo, nos ajudou com o algoritmo heurístico
import heapq

# Estado que estamos buscando
estado_final = [
    [1, 2, 3],
    [4, 8, 7],
    [6, 5, 0]
]

# Função que verifica se o estado atual é igual ao estado final
def e_final(estado):
    return estado == estado_final

# Função que retorna a posição de um determinado valor/estado
def obterPosicao(valor, estado):
    for i in range(3):
        for j in range(3):
            if estado[i][j] == valor:
                return (i, j)
    return None

# Função que calcula a distância de Manhattan
def distancia_manhattan(estado):
    distancia = 0
    for num in range(1, 9):
        posicao_atual = obterPosicao(num, estado)
        posicao_destino = obterPosicao(num, estado_final)
        distancia += abs(posicao_atual[0] - posicao_destino[0]) + abs(posicao_atual[1] - posicao_destino[1])
    return distancia

# Função que calcula o número de peças que não estão em seu estado final
def numeroPecasFora(estado):
    return sum(1 for i in range(3) for j in range(3) if estado[i][j] != estado_final[i][j] and estado[i][j] != 0)

# Função para geração de movimentos a partir de um estado
def gerarMovimentos(estado):
    linha, col = obterPosicao(0, estado)
    movimentos = []
    for dlinha, dcol in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nova_linha, nova_col = linha + dlinha, col + dcol
        if 0 <= nova_linha < 3 and 0 <= nova_col < 3:
            novo_estado = [list(r) for r in estado]
            novo_estado[linha][col], novo_estado[nova_linha][nova_col] = novo_estado[nova_linha][nova_col], novo_estado[linha][col]
            movimentos.append(novo_estado)
    return movimentos

# Função que retorna o estado atual do Puzzle no console
def print_estado(estado):
    for linha in estado:
        print(" ".join(str(x) for x in linha))
    print("----")

# Função de busca horizontal
def buscaHorizontal(estado_inicial,num_movimentos):
    tempo_inicio = time.time()
    fila = [(estado_inicial, 0)]
    passou = set()
    passou.add(str(estado_inicial))
    estados_visitados = 0

    while fila:
        estado, profundidade = fila.pop(0)
        estados_visitados += 1
        num_movimentos +=1

        print(f"Movimento {num_movimentos}:")
        print_estado(estado)

        if e_final(estado):
            tempo_decorrido = time.time() - tempo_inicio
            return profundidade, estados_visitados, tempo_decorrido

        for movimento in gerarMovimentos(estado):
            if str(movimento) not in passou:
                passou.add(str(movimento))
                fila.append((movimento, profundidade + 1))

    return None

# Função de busca heuristica
def buscaHeuristica(estado_inicial,num_movimentos):
    tempo_inicio = time.time()
    fila = []
    heapq.heappush(fila, (0, estado_inicial, 0))
    passou = set()
    passou.add(str(estado_inicial))
    estados_visitados = 0

    while fila:
        f, estado, profundidade = heapq.heappop(fila)
        estados_visitados += 1
        num_movimentos +=1

        print(f"Movimento {num_movimentos}:")
        print_estado(estado)

        if e_final(estado):
            tempo_decorrido = time.time() - tempo_inicio
            return profundidade, estados_visitados, tempo_decorrido

        for movimento in gerarMovimentos(estado):
            if str(movimento) not in passou:
                passou.add(str(movimento))
                g = profundidade + 1
                h = numeroPecasFora(movimento) + distancia_manhattan(movimento)
                f = g + h
                heapq.heappush(fila, (f, movimento, g))

    return None

# Função para testar os dois algoritmos
def testarAlgoritmo():
    # Estado em que as buscas irão iniciar
    estado_inicial = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    print("Busca Horizontal:")
    resultado_buscaHorizontal = buscaHorizontal(estado_inicial,0)
    print(f"buscaHorizontal - Profundidade da Solução: {resultado_buscaHorizontal[0]}, Estados Expandidos: {resultado_buscaHorizontal[1]}, Tempo: {resultado_buscaHorizontal[2]:.4f} segundos\n")

    print("Busca Heuristica:")
    resultado_buscaHeuristica = buscaHeuristica(estado_inicial,0)
    print(f"buscaHeuristica - Profundidade da Solução: {resultado_buscaHeuristica[0]}, Estados Expandidos: {resultado_buscaHeuristica[1]}, Tempo: {resultado_buscaHeuristica[2]:.4f} segundos")

# Main - chama a função de teste
testarAlgoritmo()
