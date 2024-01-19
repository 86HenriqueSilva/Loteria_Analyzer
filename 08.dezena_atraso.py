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

    # Menu para escolher qual prêmio analisar
    while True:
        print("Menu de Análise de Prêmios:")
        print("1 - 1º Prêmio")
        print("2 - 2º Prêmio")
        print("3 - 3º Prêmio")
        print("4 - 4º Prêmio")
        print("5 - 5º Prêmio")
        print("0 - Sair")
        opcao = int(input("Escolha a opção de prêmio para análise: "))

        if opcao == 0:
            break

        if opcao < 1 or opcao > 5:
            print("Opção inválida. Escolha um número entre 1 e 5.")
            continue

        premio_analisar = f'Prêmio{opcao}'
        premio_numero = opcao

        # Contador para a quantidade de vezes que o prêmio foi sorteado
        contagem_premio = 0

        # Lista para armazenar os resultados
        resultados = []

        # Variável para armazenar o último concurso em que a dezena foi sorteada
        ultimo_concurso = None

        # Itera pelas linhas do DataFrame em ordem inversa (do último para o primeiro)
        for index, row in dataframe.iterrows():
            concurso = row['Concurso']
            premio = row[premio_analisar]
            if premio % 100 == dezena_analisar:
                if ultimo_concurso is not None:
                    atraso = concurso - ultimo_concurso - 1  # Calcula o atraso em relação ao último concurso
                else:
                    atraso = 0
                ultimo_concurso = concurso
                contagem_premio += 1
                data = row['Data']
                data_obj = datetime.strptime(data, '%d/%m/%Y')
                dia_semana = data_obj.strftime('%A')
                resultados.append({'Concurso': concurso, 'Data': data, 'Dia da Semana': dia_semana, 'Atraso': atraso})

        # Calcula o atraso até o concurso atual
        concurso_atual = dataframe['Concurso'].iloc[-1]
        atraso_atual = concurso_atual - ultimo_concurso - 1

        # Exibe os resultados
        if resultados:
            print(f"Resultados para o {premio_numero}º Prêmio com a dezena {dezena_analisar}:")
            for resultado in resultados:
                print(
                    f"{resultado['Concurso']}, {resultado['Data']}, {resultado['Dia da Semana']}, Atraso: {resultado['Atraso']} concursos")
            print(f"Concurso atual {concurso_atual} - {ultimo_concurso} = {atraso_atual} concursos em atraso.")
            print(f"O {premio_numero}º Prêmio com a dezena {dezena_analisar} foi sorteado {contagem_premio} vezes.")
        else:
            print(f"O {premio_numero}º Prêmio com a dezena {dezena_analisar} não foi encontrado nos prêmios.")

        # Mostra a quantidade de linhas analisadas
        print(f"Quantidade de linhas analisadas: {len(dataframe)}")

except FileNotFoundError:
    print(f"O arquivo '{caminho_arquivo}' não foi encontrado.")
except Exception as e:
    print("Ocorreu um erro durante a leitura do arquivo:", e)
