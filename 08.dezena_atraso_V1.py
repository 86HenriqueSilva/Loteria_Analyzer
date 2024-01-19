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

    # Menu para escolher qual prêmio analisar
    premio_numero = int(input("Digite o número do prêmio que deseja analisar (1 a 5): "))
    if premio_numero < 1 or premio_numero > 5:
        print("Número de prêmio inválido. Deve estar entre 1 e 5.")
    else:
        print(f"Analisando o {premio_numero}º Prêmio:")
        resultados = []

        for dezena_analisar in range(0, 100):
            # Variável para armazenar o último resultado mais recente
            ultimo_resultado = None

            # Itera pelas linhas do DataFrame em ordem inversa (do último para o primeiro)
            for index, row in dataframe.iterrows():
                concurso = row['Concurso']
                premio = row[f'Prêmio{premio_numero}']
                if premio % 100 == dezena_analisar:
                    data = row['Data']
                    data_obj = datetime.strptime(data, '%d/%m/%Y')
                    dia_semana = data_obj.strftime('%A')
                    ultimo_resultado = {'Concurso': concurso, 'Data': data, 'Dia da Semana': dia_semana}

            # Adiciona o resultado à lista de resultados
            if ultimo_resultado:
                resultados.append((dezena_analisar, ultimo_resultado))

        # Ordena os resultados em ordem cronológica, do mais recente para o mais antigo
        resultados.sort(key=lambda x: x[1]['Concurso'], reverse=True)

        # Exibe os resultados
        for dezena, resultado in resultados:
            print(f"Dezena {dezena:02}: Resultado mais recente - Concurso {resultado['Concurso']}, Data {resultado['Data']}, Dia da Semana {resultado['Dia da Semana']}")

        # Mostra a quantidade de linhas analisadas
        print(f"Quantidade de linhas analisadas: {len(dataframe)}")

except FileNotFoundError:
    print(f"O arquivo '{caminho_arquivo}' não foi encontrado.")
except Exception as e:
    print("Ocorreu um erro durante a leitura do arquivo:", e)
