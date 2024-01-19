import pandas as pd
from datetime import datetime
import locale

# Define o locale para português
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

# Caminho completo para o arquivo CSV
caminho_arquivo = "/home/henrique/Documentos/Projeto Análise de Dados/federal.csv"

# Lê o arquivo CSV usando o pandas
try:
    dataframe = pd.read_csv(caminho_arquivo)

    # Pergunta ao usuário qual dezena ele gostaria de analisar
    dezena_analisar = int(input("Qual dezena você gostaria de analisar? (00-99): "))

    # Contador para a quantidade de vezes que a dezena foi sorteada
    contagem_dezena = 0

    # Lista para armazenar os resultados
    resultados = []

    # Mapeia os prêmios
    premio_numero = {1: '1º Prêmio', 2: '2º Prêmio', 3: '3º Prêmio', 4: '4º Prêmio', 5: '5º Prêmio'}

    # Itera pelas linhas do DataFrame
    for index, row in dataframe.iterrows():
        concurso = row['Concurso']
        data = row['Data']
        premios = []
        for i in range(1, 6):
            premio = row[f'Prêmio{i}']
            if premio % 100 == dezena_analisar:
                premios.append((premio, premio_numero[i]))
                contagem_dezena += 1
        if premios:
            data_obj = datetime.strptime(data, '%d/%m/%Y')
            dia_semana = data_obj.strftime('%A')
            resultados.append({'Concurso': concurso, 'Data': data, 'Dia da Semana': dia_semana, 'Prêmios': premios})

    # Exibe os resultados
    if resultados:
        print(f"Resultados para a dezena {dezena_analisar}:")
        for resultado in resultados:
            premios_formatados = ', '.join([f"{premio[1]} {premio[0]}" for premio in resultado['Prêmios']])
            print(f"{resultado['Concurso']}, {resultado['Data']}, {resultado['Dia da Semana']}, {premios_formatados}")
        print(f"A dezena {dezena_analisar} foi sorteada {contagem_dezena} vezes.")
    else:
        print(f"A dezena {dezena_analisar} não foi encontrada nos prêmios.")

    # Mostra a quantidade de linhas analisadas
    print(f"Quantidade de linhas analisadas: {len(dataframe)}")

except FileNotFoundError:
    print(f"O arquivo '{caminho_arquivo}' não foi encontrado.")
except Exception as e:
    print("Ocorreu um erro durante a leitura do arquivo:", e)
