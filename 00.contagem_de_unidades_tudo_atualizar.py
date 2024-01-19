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

except FileNotFoundError:
    print(f"Arquivo não encontrado: {caminho_arquivo}")
    exit()

# Exportar dados para o Pandas DataFrame
df = pd.DataFrame(dados_csv)

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

def menu():
    while True:
        print("Menu:")
        print("1. Análise de Unidades / Extração 1º")
        print("2. Análise de Unidades / Extração 2º")
        print("3. Análise de Unidades / Extração 3º")
        print("4. Análise de Unidades / Extração 4º")
        print("5. Análise de Unidades / Extração 5º")
        print("6. Adicionar dados")
        print("7. Deletar dados (múltiplos concursos, separados por vírgula)")
        print("8. Exibir todos os dados")
        print("0. Sair")
        escolha = input("Por Favor Digite Uma Das Opções do Menu (0-8): ")

        if escolha == "1" or escolha == "2" or escolha == "3" or escolha == "4" or escolha == "5":
            escolha = int(escolha)
            contador, total_linhas_analisadas = contar_numeros(df, escolha)
            for j in range(10):
                for i, contagem in enumerate(contador):
                    print(f"{j}:{contagem[j]}X", end=" ")
                print("\n")
            print(f"Total de linhas analisadas: {total_linhas_analisadas}")
        elif escolha == "6":
            adicionar_dados()
        elif escolha == "7":
            deletar_dados()
        elif escolha == "8":
            exibir_dados()
        elif escolha == "0":
            break
        else:
            print("Opção inválida. Por favor, escolha novamente.")

def adicionar_dados():
    global df
    concurso = input("Número(s) do(s) Concurso(s) (separados por vírgula e espaço, limite de 10): ")
    concursos = [int(c.strip()) for c in concurso.split(",") if c.strip().isdigit()]

    if not concursos:
        print("Nenhum concurso válido foi informado.")
        return

    novos_dados = []
    for c in concursos:
        if c in df['Concurso'].values:
            print(f"Concurso {c} já existe no arquivo. Os dados não serão adicionados.")
        else:
            data = input(f"Data do Concurso {c} (formato dd/mm/yyyy): ")
            try:
                data_convertida = datetime.strptime(data, '%d/%m/%Y').strftime('%d/%m/%Y')
                premio1 = ajustar_resultado(input("Prêmio 1: "))
                premio2 = ajustar_resultado(input("Prêmio 2: "))
                premio3 = ajustar_resultado(input("Prêmio 3: "))
                premio4 = ajustar_resultado(input("Prêmio 4: "))
                premio5 = ajustar_resultado(input("Prêmio 5: "))
                novos_dados.append([c, data_convertida, premio1, premio2, premio3, premio4, premio5])
            except ValueError:
                print("Data inválida. Utilize o formato dd/mm/yyyy.")
                return

    if novos_dados:
        with open(caminho_arquivo, 'a', newline='') as arquivo_csv:
            escrever_csv = csv.writer(arquivo_csv)
            for linha in novos_dados:
                escrever_csv.writerow(linha)

        print("Dados adicionados com sucesso!")
        # Atualizar o DataFrame com os dados após a adição
        df = pd.read_csv(caminho_arquivo)
        exibir_dados()

def deletar_dados():
    global df
    try:
        concursos_para_deletar = input("Digite os números dos concursos que deseja deletar "
                                      "(separados por vírgula e espaço, limite de 10): ")
        concursos = [int(c.strip()) for c in concursos_para_deletar.split(",") if c.strip().isdigit()]

        if not concursos:
            print("Nenhum concurso válido foi informado.")
            return

        df_concursos = df['Concurso'].values
        for c in concursos:
            if c not in df_concursos:
                print(f"Concurso {c} não encontrado. Nenhum dado será deletado.")
                return

        df = df[~df['Concurso'].isin(concursos)]

        # Salvar a alteração no arquivo CSV
        df.to_csv(caminho_arquivo, index=False)

        print("Dados deletados com sucesso!")
        # Atualizar o DataFrame com os dados após a exclusão
        df = pd.read_csv(caminho_arquivo)
        exibir_dados()

    except ValueError:
        print("Entrada inválida. Digite números válidos, separados por vírgula e espaço.")

def exibir_dados():
    df = pd.read_csv(caminho_arquivo)
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')  # Convert the 'Data' column to datetime format
    df = df.sort_values(by=['Data', 'Concurso'])  # Sort DataFrame by 'Data' and then by 'Concurso'
    pd.set_option('display.max_rows', None)  # To display all rows of the DataFrame
    print(df)

menu()  # Chamar a função do menu para começar a interação
