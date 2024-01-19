import csv


def par_ou_impar(numero):
    if numero.isdigit():
        if int(numero) % 2 == 0:
            return 'par'
        else:
            return 'ímpar'
    else:
        return numero


caminho_arquivo_entrada = '/home/henrique/Documentos/Projeto Análise de Dados/conversao_grupos.csv'
caminho_arquivo_saida = '/home/henrique/Documentos/Projeto Análise de Dados/conversao_de_dezenas_par_impar.csv'

dados_processados = []

# Abre o arquivo CSV de entrada no modo de leitura
with open(caminho_arquivo_entrada, 'r', newline='', encoding='utf-8') as arquivo_csv:
    leitor_csv = csv.reader(arquivo_csv)

    # Itera sobre as linhas do arquivo CSV
    for indice, linha in enumerate(leitor_csv):
        if indice == 0:
            dados_processados.append(linha)  # Mantém a primeira linha (títulos)
        else:
            linha_processada = linha[:2]  # Mantém os primeiros dois elementos
            for numero in linha[2:]:
                linha_processada.append(par_ou_impar(numero))
            dados_processados.append(linha_processada)

# Escreve os dados processados em um novo arquivo CSV de saída
with open(caminho_arquivo_saida, 'w', newline='', encoding='utf-8') as arquivo_saida:
    escritor_csv = csv.writer(arquivo_saida)
    for linha in dados_processados:
        escritor_csv.writerow(linha)

# Imprime os dados processados
for linha in dados_processados:
    print(linha)

print("Arquivo CSV de saída criado em:", caminho_arquivo_saida)
