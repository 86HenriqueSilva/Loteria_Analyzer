import pandas as pd
from datetime import datetime
import locale
import os

# Define o locale para português
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

# Caminho completo para o arquivo CSV
caminho_arquivo = "/home/henrique/Documentos/Projeto Análise de Dados/federal.csv"
diretorio_relatorios = "/home/henrique/Documentos/Projeto Análise de Dados/Relatorios/"

# Certifique-se de que o diretório de relatórios exista
if not os.path.exists(diretorio_relatorios):
    os.makedirs(diretorio_relatorios)

# Lê o arquivo CSV usando o pandas
try:
    dataframe = pd.read_csv(caminho_arquivo)

    # Menu para escolher qual prêmio analisar
    premio_numero = int(input("Digite o número do prêmio que deseja analisar (1 a 5): "))
    if premio_numero < 1 or premio_numero > 5:
        print("Número de prêmio inválido. Deve estar entre 1 e 5.")
    else:
        nome_relatorio = f"RELATORIO_DEZENAS_ATRAZADAS_{premio_numero}.CSV"
        caminho_relatorio = os.path.join(diretorio_relatorios, nome_relatorio)
        print(f"Analisando o {premio_numero}º Prêmio e salvando como '{caminho_relatorio}':")
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

        # Cria um DataFrame para os resultados
        df_resultados = pd.DataFrame(resultados, columns=['Dezena', 'Resultado'])

        # Salva o DataFrame como um arquivo CSV no diretório de relatórios
        df_resultados.to_csv(caminho_relatorio, index=False)

        # Exibe os resultados
        for dezena, resultado in resultados:
            print(f"Dezena {dezena:02}: Resultado mais recente - Concurso {resultado['Concurso']}, Data {resultado['Data']}, Dia da Semana {resultado['Dia da Semana']}")

        print(f"Relatório salvo em {caminho_relatorio}")

except FileNotFoundError:
    print(f"O arquivo '{caminho_arquivo}' não foi encontrado.")
except Exception as e:
    print("Ocorreu um erro durante a leitura do arquivo:", e)
