import csv

# Caminho para o arquivo CSV
caminho_arquivo = '/home/henrique/Documentos/Projeto Análise de Dados/federal.csv'
caminho_saida = '/home/henrique/Documentos/Projeto Análise de Dados/nao_sorteados.csv'

# Conjunto para armazenar os números sorteados
numeros_sorteados = set()

# Realizando a leitura do arquivo CSV e armazenando os números sorteados
with open(caminho_arquivo, 'r') as arquivo:
    leitor_csv = csv.reader(arquivo)
    next(leitor_csv)  # Pular a primeira linha (cabeçalho)
    for linha in leitor_csv:
        for i in range(1, 6):  # Considerando os cinco prêmios
            try:
                numero_sorteado = int(linha[i])  # Tentar converter para inteiro
                numeros_sorteados.add(numero_sorteado)
            except ValueError:
                pass  # Ignorar linhas inválidas

# Encontrando os números ausentes
numeros_ausentes = set(range(10000)) - numeros_sorteados

# Ordenando os números ausentes
numeros_ausentes_ordenados = sorted(numeros_ausentes)

# Salvando os números ausentes em um arquivo CSV
with open(caminho_saida, 'w', newline='') as arquivo_saida:
    escritor_csv = csv.writer(arquivo_saida)
    escritor_csv.writerow(['Numeros_Ausentes'])
    for numero in numeros_ausentes_ordenados:
        escritor_csv.writerow([numero])

print(f"Total de números não sorteados: {len(numeros_ausentes_ordenados)}")
print(f"Os números não sorteados foram salvos em: {caminho_saida}")
