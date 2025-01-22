import recomendador as r
import random
import math
import time

def readDataset(filename):
    arestas = []

    with open(filename, 'r') as file:
        for line in file:
            vert1, vert2, _, _ = line.split(" ")
            arestas.append((int(vert1), int(vert2)))

    return arestas

def writeResults(parameters, results, usuarios, numDados, filename):
    totalExecTime = 0
    totalPrecision = 0
    totalRecall = 0
    totalF1Score = 0

    with open(filename, 'w') as file:
        file.write("Parametros: \n" +
                   f"Numero de passeios por usuario: {parameters[0]}\n" +
                   f"Comprimento dos passeios: {parameters[1]}\n" +
                   f"Numero de Recomendacoes: {parameters[2]}\n" +
                   f"Numero de Usuarios: {parameters[3]}\n\n")
        
        for i in range(numDados):
            execTime, precision, recall, f1Score = results[i]
            file.write(f"Usuario: {usuarios[i]}\n" +
                       f"Tempo de Execucao: {execTime}\n" +
                       f"Precision: {precision} // Recall: {recall} // F1-Score: {f1Score}\n\n")
            
            totalExecTime += execTime
            totalPrecision += precision
            totalRecall += recall
            totalF1Score += f1Score
        
        mediaExecTime = totalExecTime/numDados
        mediaPrecision = totalPrecision/numDados
        mediaRecall = totalRecall/numDados
        mediaF1Score = totalF1Score/numDados
        file.write(f"Media de tempo de execucao: {mediaExecTime}\n" +
                   f"Media da Precisao: {mediaPrecision}\n" +
                   f"Media do Recall: {mediaRecall}\n" +
                   f"Media do F1-Score: {mediaF1Score}\n")
            

def Precision(usuariosRecomendados, recomendacoesEsperadas):
    acertos = 0
    numRecomendacoes = len(usuariosRecomendados)
    if numRecomendacoes == 0:
        return 0
    for u in usuariosRecomendados:
        if u in recomendacoesEsperadas:
            acertos += 1
    return acertos/numRecomendacoes

def Recall(usuariosRecomendados, recomendacoesEsperadas):
    acertos = 0
    numPossiveisRecomendacoes = len(recomendacoesEsperadas)
    for u in usuariosRecomendados:
        if u in recomendacoesEsperadas:
            acertos += 1
    return acertos/numPossiveisRecomendacoes

def main():
    # Configurações do algoritmo
    numPasseios = 5000
    comprimentoPasseios = 5
    numRecomendacoes = 10
    numUsuarios = 500
    inputFilename = "dataset.txt"
    outputFilename = "testes/resultadosQ3.txt"

    parameters = [numPasseios, comprimentoPasseios, numRecomendacoes, numUsuarios]

    arestas = readDataset(inputFilename)
    grafo = r.Grafo()
    grafo.criaGrafo(arestas)

    usuarios = []

    usuarios = random.sample(list(grafo.listaAdjacencia), numUsuarios)

    # Caso usuario possua apenas 1 ou 0 conexoes, descartar caso e colocar outro (restricao do algoritmo)
    for i in range(numUsuarios):
        while len(grafo.vizinhos(usuarios[i])) < 2:
            usuarios[i] = random.choice(list(grafo.listaAdjacencia))

    results = []

    for usuario in usuarios:
        amigos = grafo.vizinhos(usuario)

        # Excluir 20% dos amigos para usar no teste de precision and recall
        numAmigosExcluir = math.ceil(len(amigos) * 0.2)
        recomendacoesEsperadas = random.sample(amigos, numAmigosExcluir)
        for amigoEsperado in recomendacoesEsperadas:
            grafo.excluiAresta(usuario, amigoEsperado)

        # Ignorar recomendações de quem já é amigo e do próprio usuário
        recomendacoesAExcluir = amigos.copy()
        recomendacoesAExcluir.append(usuario)

        start_time = time.time()
        usuariosRecomendados, _ = r.recomenda(grafo, usuario, numPasseios, comprimentoPasseios, numRecomendacoes, recomendacoesAExcluir)
        end_time = time.time()

        executionTime = end_time - start_time
        precision = Precision(usuariosRecomendados, recomendacoesEsperadas)
        recall = Recall(usuariosRecomendados, recomendacoesEsperadas)
        if precision+recall == 0:
            f1Score = 0
        else:
            f1Score = (2*precision*recall)/(precision+recall)

        results.append((executionTime, precision, recall, f1Score))
        
        # Reconstruir arestas excluidas anteriormente
        for amigoEsperado in recomendacoesEsperadas:
            grafo.adicionaAresta(usuario, amigoEsperado)
    
    writeResults(parameters, results, usuarios, numUsuarios, outputFilename)

if __name__ == "__main__":
    main()