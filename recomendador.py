import random

class Grafo:
    def __init__(self):
        self.listaAdjacencia = {}
    
    def adicionaAresta(self, vert1: int, vert2: int):
        if vert1 not in self.listaAdjacencia:
            self.listaAdjacencia[vert1] = []
        if vert2 not in self.listaAdjacencia:
            self.listaAdjacencia[vert2] = []
        self.listaAdjacencia[vert1].append(vert2)
        self.listaAdjacencia[vert2].append(vert1)
    
    def excluiAresta(self, vert1: int, vert2: int):
        if vert1 in self.listaAdjacencia and vert2 in self.listaAdjacencia[vert1]:
            self.listaAdjacencia[vert1].remove(vert2)
        if vert2 in self.listaAdjacencia and vert1 in self.listaAdjacencia[vert2]:
            self.listaAdjacencia[vert2].remove(vert1)
    
    def criaGrafo(self, arestas: list[(int, int)]):
        for vert1, vert2 in arestas:
            self.adicionaAresta(vert1, vert2)
    
    def vizinhos(self, vertice: int):
        return self.listaAdjacencia.get(vertice, [])

# Passeio Aleatório
def passeioAleatorio(grafo: Grafo, verticeInicial: int, comprimento: int) -> list[int]:
    passeio = []
    verticeAtual = verticeInicial
    verticeAnterior = None

    for _ in range(comprimento):
        passeio.append(verticeAtual)
        vizinhos = grafo.vizinhos(verticeAtual)
        vizinhosValidos = [v for v in vizinhos if v != verticeAnterior] # Durante o passeio, não voltar imediatamente para o vértice de onde veio

        if not vizinhosValidos: # caso o vértice não possua vizinhos válidos, encerrar este passeio
            break

        proximoVertice = random.choice(vizinhos)
        verticeAnterior = verticeAtual
        verticeAtual = proximoVertice
    
    return passeio

# Interseções de passeios aleatórios
def intersecaoPasseiosAleatorios(grafo: Grafo, verticeInicial: int, numPasseios: int, comprimento: int) -> dict[int, int]:
    frequenciaVertices = {}
    for _ in range(numPasseios):
        passeio = passeioAleatorio(grafo, verticeInicial, comprimento)
        for vertice in passeio:
            if vertice in frequenciaVertices:
                frequenciaVertices[vertice] += 1
            else:
                frequenciaVertices[vertice] = 1

    return frequenciaVertices

# Recomendações
def recomenda(grafo: Grafo, verticeInicial: int, numPasseios: int, comprimento: int, numRecomendacoes: int, verticesAExcluir: list[int] = []):
    
    frequenciaVertices = intersecaoPasseiosAleatorios(grafo, verticeInicial, numPasseios, comprimento)
    recomendacoes = [
        (vertice, frequencia) for vertice, frequencia in frequenciaVertices.items() if vertice not in verticesAExcluir
    ]
    recomendacoes.sort(key=lambda x: x[1], reverse=True)  # Ordenar por frequência
    recomendacoes = recomendacoes[:numRecomendacoes]
    usuarios = []
    pontuacoes = []
    for usuario, pontuacao in recomendacoes:
        usuarios.append(usuario)
        pontuacoes.append(pontuacao)
    
    return usuarios, pontuacoes

# Exemplo de Uso
def main():
    grafo = Grafo()
    arestas = [
        (1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7),
        (4, 8), (5, 8), (6, 9), (7, 9), (8, 10), (9, 10)
    ]
    grafo.criaGrafo(arestas)
    
    # Configurações do algoritmo
    verticeInicial = 1 # Usuario a receber recomendacoes
    numPasseios = 1000
    comprimentoPasseios = 5
    numRecomendacoes = 5
    recomendacoesAExcluir = grafo.vizinhos(verticeInicial)
    recomendacoesAExcluir.append(verticeInicial)
    
    usuariosRecomendados, pontuacaoUsuarios = recomenda(grafo, verticeInicial, numPasseios, comprimentoPasseios, numRecomendacoes, recomendacoesAExcluir)
    
    print("\nRecomendações baseadas em interseções de passeios aleatórios:")
    for i in range(numRecomendacoes):
        print(f"Usuário: {usuariosRecomendados[i]}, Pontuação: {pontuacaoUsuarios[i]}")
    print()

if __name__ == "__main__":
    main()