import csv
import pandas as pd
from datetime import datetime

# Função para ajustar os resultados com 4 dígitos e substituir "mio" por "prêmio"
def ajustar_resultado(resultado):
    resultado = resultado.replace("mio", "Prêmio")  # Substitui "mio" por "Prêmio"
    resultado = resultado[-4:]  # Obtém os últimos 4 dígitos do resultado
    return resultado.zfill(4)

# Dicionário para armazenar os dados do CSV
dados_csv = {'Concurso': [], 'Data': [], 'Prêmio1': [], 'Prêmio2': [], 'Prêmio3': [], 'Prêmio4': [], 'Prêmio5': []}

# Caminho do arquivo CSV
caminho_arquivo = '/home/henrique/Documentos/Projeto Análise de Dados/federal.csv'

# Função para converter a data no formato "dd/mm/yyyy" para "dd/mm/yyyy"
def converter_data(data):
    return data

# Abre o arquivo CSV em modo de leitura
try:
    with open(caminho_arquivo, 'r') as arquivo_csv:
        # Cria um objeto leitor do CSV
        leitor_csv = csv.reader(arquivo_csv)

        # Pula a primeira linha (cabeçalho) do arquivo CSV
        next(leitor_csv)

        # Itera sobre as linhas do CSV e armazena os dados no dicionário
        for linha in leitor_csv:
            if len(linha) >= 7:  # Verifica se a linha tem o número correto de elementos
                dados_csv['Concurso'].append(int(linha[0]))
                dados_csv['Data'].append(converter_data(linha[1]))
                dados_csv['Prêmio1'].append(ajustar_resultado(linha[2]))
                dados_csv['Prêmio2'].append(ajustar_resultado(linha[3]))
                dados_csv['Prêmio3'].append(ajustar_resultado(linha[4]))
                dados_csv['Prêmio4'].append(ajustar_resultado(linha[5]))
                dados_csv['Prêmio5'].append(ajustar_resultado(linha[6]))
            else:
                print(f"Linha ignorada: {linha}")

    # Exportar dados para o Pandas DataFrame e converter a coluna 'Data'
    df = pd.DataFrame(dados_csv)
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')

except FileNotFoundError:
    print(f"Arquivo não encontrado: {caminho_arquivo}")
    exit()

def contar_numeros(df, extracao):
    contadores = [[0] * 10 for _ in range(4)]  # Inicializa os contadores para os números de 0 a 9 para as quatro listas
    numeros = df[f'Prêmio{extracao}'].tolist()
    total_linhas_analisadas = len(numeros)

    for numero_str in numeros:
        for i, digito_str in enumerate(numero_str):
            if digito_str.isdigit():
                digito = int(digito_str)
                contadores[i][digito] += 1

    return contadores, total_linhas_analisadas

def obter_periodo():
    while True:
        try:
            inicio = int(input("Digite o ano de início do período de análise: "))
            fim = int(input("Digite o ano de fim do período de análise: "))
            if inicio <= fim:
                return inicio, fim
            else:
                print("O ano de início deve ser menor ou igual ao ano de fim.")
        except ValueError:
            print("Por favor, digite anos válidos.")

def analisar_por_extracao():
    while True:
        try:
            extracao = int(input("Digite a extração desejada (1 a 5): "))
            if extracao in [1, 2, 3, 4, 5]:
                break
            else:
                print("Escolha uma extração válida (1 a 5).")
        except ValueError:
            print("Por favor, digite um número válido (1 a 5).")

    inicio, fim = obter_periodo()
    df_periodo = df[(df['Data'].dt.year >= inicio) & (df['Data'].dt.year <= fim)]

    contador, total_linhas_analisadas = contar_numeros(df_periodo, extracao)
    print(f"Análise para a Extração {extracao} no período de {inicio} a {fim}:")
    for j in range(10):
        for i, contagem in enumerate(contador):
            print(f"{j}:{contagem[j]}X", end=" ")
        print("\n")
    print(f"Total de linhas analisadas: {total_linhas_analisadas}")

# Atualização da função menu()
def menu():
    while True:
        print("Menu:")
        print("1. Análise por extração")
        print("2. Adicionar dados")
        print("3. Deletar dados (múltiplos concursos, separados por vírgula)")
        print("4. Exibir todos os dados")
        print("0. Sair")
        escolha = input("Por Favor Digite Uma Das Opções do Menu (0-4): ")

        if escolha == "1":
            analisar_por_extracao()
        elif escolha == "2":
            adicionar_dados()
        elif escolha == "3":
            deletar_dados()
        elif escolha == "4":
            exibir_dados()
        elif escolha == "0":
            break
        else:
            print("Opção inválida. Por favor, escolha novamente.")

menu()


