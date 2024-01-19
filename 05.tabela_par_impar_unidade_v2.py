import csv
from collections import Counter
from datetime import datetime


def criar_combinacoes():
    combinacoes = []

    for i in ["I", "P"]:
        for j in ["I", "P"]:
            for k in ["I", "P"]:
                for l in ["I", "P"]:
                    combinacoes.append(i + j + k + l)

    return combinacoes


def ler_arquivo_csv(caminho_arquivo):
    dados = []

    try:
        with open(caminho_arquivo, 'r') as arquivo_csv:
            leitor_csv = csv.reader(arquivo_csv)
            cabecalho = next(leitor_csv)  # Lê o cabeçalho do CSV

            for linha in leitor_csv:
                dados.append(linha)

    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho_arquivo}")

    return cabecalho, dados


def contar_combinacoes_premio(premio):
    combinacoes = criar_combinacoes()
    contagem = Counter()

    for linha in dados:
        numeros_convertidos = ajustar_resultado(linha[2 + premio])
        contagem[numeros_convertidos] += 1

    print("   ", end="")
    for combinacao in combinacoes:
        print(combinacao, end="   ")
    print()  # Pula uma linha para a próxima linha

    for combinacao in combinacoes:
        quantidade = contagem[combinacao]
        print(f"{combinacao}: {quantidade} vezes")


def converter_numero(numero):
    return "I" if int(numero) % 2 != 0 else "P"


def ajustar_resultado(resultado):
    resultado = resultado.replace("mio", "Prêmio")
    return resultado.zfill(4)


caminho_arquivo_csv = '/home/henrique/Documentos/Projeto Análise de Dados/conversao_p_i.csv'
cabecalho, dados = ler_arquivo_csv(caminho_arquivo_csv)

while True:
    print("\nMenu:")
    print("1. Análise de P/I Extração 1º")
    print("2. Análise de P/I Extração 2º")
    print("3. Análise de P/I Extração 3º")
    print("4. Análise de P/I Extração 4º")
    print("5. Análise de P/I Extração 5º")
    print("0. Sair")

    escolha = input("Escolha uma opção: ")

    if escolha == "0":
        break
    elif escolha in ["1", "2", "3", "4", "5"]:
        premio_selecionado = int(escolha) - 1
        contar_combinacoes_premio(premio_selecionado)
    else:
        print("Opção inválida. Escolha novamente.")
