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

    # Dicionário para armazenar as contagens de cada dezena
    contagem_dezenas = {dezena: 0 for dezena in range(100)}

    # Mapeia os prêmios
    premio_numero = {1: '1º Prêmio', 2: '2º Prêmio', 3: '3º Prêmio', 4: '4º Prêmio', 5: '5º Prêmio'}

    # Itera pelas linhas do DataFrame
    for index, row in dataframe.iterrows():
        for i in range(1, 6):
            premio = row[f'Prêmio{i}']
            dezena_analisar = premio % 100
            contagem_dezenas[dezena_analisar] += 1

    # Exibe os resultados para cada dezena
    for dezena, contagem in contagem_dezenas.items():
        print(f"Dezena {dezena:02d} foi sorteada {contagem} vezes.")

    # Encontra as 10 dezenas mais sorteadas e as 10 menos sorteadas
    top_mais_sorteadas = sorted(contagem_dezenas.items(), key=lambda x: x[1], reverse=True)[:10]
    top_menos_sorteadas = sorted(contagem_dezenas.items(), key=lambda x: x[1])[:10]

    # Exibe o top 10 mais sorteadas
    print("\nTop 10 Mais Sorteadas:")
    for dezena, contagem in top_mais_sorteadas:
        print(f"Dezena {dezena:02d}: {contagem} vezes")

    # Exibe o top 10 menos sorteadas
    print("\nTop 10 Menos Sorteadas:")
    for dezena, contagem in top_menos_sorteadas:
        print(f"Dezena {dezena:02d}: {contagem} vezes")

    # Mostra a quantidade de linhas analisadas
    print(f"\nQuantidade de linhas analisadas: {len(dataframe)}")

except FileNotFoundError:
    print(f"O arquivo '{caminho_arquivo}' não foi encontrado.")
except Exception as e:
    print("Ocorreu um erro durante a leitura do arquivo:", e)
