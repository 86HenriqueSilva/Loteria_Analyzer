import csv
import pandas as pd
from collections import Counter


def ajustar_resultado(resultado):
    resultado = resultado.replace("mio", "Prêmio")
    resultado = resultado[-4:]
    return resultado.zfill(4)


def converter_data(data):
    dia, mes, ano = data.split('/')
    return f"{ano}-{mes.zfill(2)}-{dia.zfill(2)}"


def atraso_de_dezena(dezena, numeros):
    atraso = 0
    for numero_str in numeros:
        if dezena in numero_str:
            return atraso
        atraso += 1
    return None


def analisar_dezenas(df, extracao):
    numeros = df[f'Prêmio{extracao}'].tolist()
    atrasos = {}

    for dezena in range(100):
        dezena_str = str(dezena).zfill(2)
        atraso = atraso_de_dezena(dezena_str, numeros)
        if atraso is not None:
            atrasos[dezena_str] = atraso

    return atrasos


# Restante do código permanece o mesmo

def menu():
    while True:
        print("Menu:")
        print("1. Análise de Unidades / Extração 1º")
        print("2. Análise de Unidades / Extração 2º")
        print("3. Análise de Unidades / Extração 3º")
        print("4. Análise de Unidades / Extração 4º")
        print("5. Análise de Unidades / Extração 5º")
        print("0. Sair")
        escolha = input("Escolha a Extração para Análise de dados (0-5): ")

        if escolha == "1" or escolha == "2" or escolha == "3" or escolha == "4" or escolha == "5":
            escolha = int(escolha)
            atrasos = analisar_dezenas(df, escolha)

            # Contagem de frequência das dezenas
            numeros = df[f'Prêmio{escolha}'].str.findall(r'\d{2}').sum()
            frequencia_dezenas = Counter(numeros)
            mais_frequentes = frequencia_dezenas.most_common(10)

            # Dezenas mais atrasadas
            dezenas_ausentes = set([str(i).zfill(2) for i in range(100)]) - set(atrasos.keys())
            dezenas_ausentes_atraso = [(dezena, None) for dezena in dezenas_ausentes]
            mais_atrasados = list(atrasos.items()) + dezenas_ausentes_atraso
            mais_atrasados.sort(key=lambda x: x[1], reverse=True)
            mais_atrasados = mais_atrasados[:10]

            print("\nDezenas mais frequentes:")
            for dezena, freq in mais_frequentes:
                print(f"Dezena: {dezena} | Frequência: {freq}")

            print("\nDezenas mais atrasadas:")
            for dezena, atraso in mais_atrasados:
                print(f"Dezena: {dezena} | Atraso: {atraso}")

        elif escolha == "0":
            break
        else:
            print("Opção inválida. Por favor, escolha novamente.")


# Leitura e processamento do arquivo CSV
dados_csv = {'Concurso': [], 'Data': [], 'Prêmio1': [], 'Prêmio2': [], 'Prêmio3': [], 'Prêmio4': [], 'Prêmio5': []}
caminho_arquivo = '/home/henrique/Documentos/Projeto Análise de Dados/federal.csv'

try:
    with open(caminho_arquivo, 'r') as arquivo_csv:
        leitor_csv = csv.reader(arquivo_csv)
        next(leitor_csv)

        for linha in leitor_csv:
            if len(linha) >= 7:
                dados_csv['Concurso'].append(linha[0])
                dados_csv['Data'].append(converter_data(linha[1]))
                dados_csv['Prêmio1'].append(ajustar_resultado(linha[2]))
                dados_csv['Prêmio2'].append(ajustar_resultado(linha[3]))
                dados_csv['Prêmio3'].append(ajustar_resultado(linha[4]))
                dados_csv['Prêmio4'].append(ajustar_resultado(linha[5]))
                dados_csv['Prêmio5'].append(ajustar_resultado(linha[6]))
            else:
                print(f"Linha ignorada: {linha}")

except FileNotFoundError:
    print(f"Arquivo não encontrado: {caminho_arquivo}")
    exit()

df = pd.DataFrame(dados_csv)

menu()
