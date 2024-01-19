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


def analisar_dezenas(df):
    atrasos_por_extracao = {}

    for extracao in range(1, 6):
        numeros = df[f'Prêmio{extracao}'].tolist()
        atrasos = {}

        for dezena in range(100):
            dezena_str = str(dezena).zfill(2)
            atraso = atraso_de_dezena(dezena_str, numeros)
            atrasos[dezena_str] = atraso

        atrasos_por_extracao[extracao] = atrasos

    return atrasos_por_extracao


def atraso_de_dezena(dezena, numeros):
    ultimo_concurso = None
    atraso = 0
    for concurso, nums in numeros.items():
        if dezena in nums:
            atraso = concurso - ultimo_concurso - 1 if ultimo_concurso is not None else 0
            ultimo_concurso = concurso
    return atraso


def menu():
    while True:
        print("Menu:")
        print("1. Análise de Unidades / Extrações 1º ao 5º")
        print("0. Sair")
        escolha = input("Escolha a opção (0 ou 1): ")

        if escolha == "1":
            atrasos_por_extracao = analisar_dezenas(df)

            for extracao, atrasos in atrasos_por_extracao.items():
                print(f"\nAnálise das dezenas para a Extração {extracao}º:")

                # Contagem de frequência das dezenas
                numeros = df[f'Prêmio{extracao}'].str.findall(r'\d{2}')
                numeros_por_concurso = {int(row['Concurso']): nums for row, nums in zip(df.to_dict('records'), numeros)}
                frequencia_dezenas = Counter(numeros)
                mais_frequentes = frequencia_dezenas.most_common(10)

                # Dezenas mais atrasadas
                mais_atrasados = sorted(atrasos.items(), key=lambda x: x[1], reverse=True)[:10]

                print("Dezenas mais frequentes:")
                for dezena, freq in mais_frequentes:
                    print(f"Dezena: {dezena} | Frequência: {freq}")

                print("Dezenas mais atrasadas:")
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
                dados_csv['Concurso'].append(int(linha[0]))
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
