import pandas as pd
import os
from babel.dates import format_date, Locale
from tabulate import tabulate

# Tabela de grupos
tabela_grupos = {
    "01": {"grupo": "AVESTRUZ", "dezenas": ["01", "02", "03", "04"]},
    "02": {"grupo": "ÁGUIA", "dezenas": ["05", "06", "07", "08"]},
    "03": {"grupo": "BURRO", "dezenas": ["09", "10", "11", "12"]},
    "04": {"grupo": "BORBOLETA", "dezenas": ["13", "14", "15", "16"]},
    "05": {"grupo": "CACHORRO", "dezenas": ["17", "18", "19", "20"]},
    "06": {"grupo": "CABRA", "dezenas": ["21", "22", "23", "24"]},
    "07": {"grupo": "CARNEIRO", "dezenas": ["25", "26", "27", "28"]},
    "08": {"grupo": "CAMELO", "dezenas": ["29", "30", "31", "32"]},
    "09": {"grupo": "COBRA", "dezenas": ["33", "34", "35", "36"]},
    "10": {"grupo": "COELHO", "dezenas": ["37", "38", "39", "40"]},
    "11": {"grupo": "CAVALO", "dezenas": ["41", "42", "43", "44"]},
    "12": {"grupo": "ELEFANTE", "dezenas": ["45", "46", "47", "48"]},
    "13": {"grupo": "GALO", "dezenas": ["49", "50", "51", "52"]},
    "14": {"grupo": "GATO", "dezenas": ["53", "54", "55", "56"]},
    "15": {"grupo": "JACARÉ", "dezenas": ["57", "58", "59", "60"]},
    "16": {"grupo": "LEÃO", "dezenas": ["61", "62", "63", "64"]},
    "17": {"grupo": "MACACO", "dezenas": ["65", "66", "67", "68"]},
    "18": {"grupo": "PORCO", "dezenas": ["69", "70", "71", "72"]},
    "19": {"grupo": "PAVÃO", "dezenas": ["73", "74", "75", "76"]},
    "20": {"grupo": "PERU", "dezenas": ["77", "78", "79", "80"]},
    "21": {"grupo": "TOURO", "dezenas": ["81", "82", "83", "84"]},
    "22": {"grupo": "TIGRE", "dezenas": ["85", "86", "87", "88"]},
    "23": {"grupo": "URSO", "dezenas": ["89", "90", "91", "92"]},
    "24": {"grupo": "VEADO", "dezenas": ["93", "94", "95", "96"]},
    "25": {"grupo": "VACA", "dezenas": ["97", "98", "99", "00"]}
}

# Configurar o Pandas para exibir todas as colunas em uma única linha
pd.set_option('display.expand_frame_repr', False)

# Substitua o caminho e o nome do arquivo conforme necessário
caminho_pasta = '/home/henrique/Documentos'
nome_arquivo = 'BASE DE DADOS.xls'  # Substitua pelo novo nome de arquivo
caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)

# Verificar se o arquivo existe antes de tentar ler
if os.path.exists(caminho_arquivo):
    # Use o método read_excel do Pandas para ler a planilha
    dados = pd.read_excel(caminho_arquivo)

    # Ajustar o formato da coluna de data
    dados['Data'] = pd.to_datetime(dados['Data'], format='%d/%m/%Y', errors='coerce').dt.date

    # Configurar local para português do Brasil
    locale = Locale('pt_BR')

    # Preencher a coluna "D/SEMAN" com o dia da semana em português
    dados['D/SEMAN'] = dados['Data'].apply(lambda x: format_date(x, 'EEEE', locale=locale))

    # Adicionar zeros à esquerda nas colunas de prêmios
    colunas_premios = ['1º PRÊMIO', '2º PRÊMIO', '3º PRÊMIO', '4º PRÊMIO', '5º PRÊMIO']
    for coluna in colunas_premios:
        dados[coluna] = dados[coluna].apply(lambda x: f'{x:04}')

    # Criar as colunas S 1º, S 2º, S 3º, S 4º, S 5º com listas de dígitos
    colunas_s = ['S 1º', 'S 2º', 'S 3º', 'S 4º', 'S 5º']
    for coluna_premio, coluna_s in zip(colunas_premios, colunas_s):
        dados[coluna_s] = dados[coluna_premio].apply(lambda x: [int(d) for d in str(x)])

    # Preencher as colunas D 1º, D 2º, D 3º, D 4º, D 5º com as posições 3 e 4 das listas em S 1º, S 2º, S 3º, S 4º, S 5º
    colunas_d = ['D 1º', 'D 2º', 'D 3º', 'D 4º', 'D 5º']
    for coluna_s, coluna_d in zip(colunas_s, colunas_d):
        dados[coluna_d] = dados[coluna_s].apply(lambda x: f"{x[2]:01}{x[3]:01}")

    # Mapear os valores das dezenas para os grupos e preencher as colunas GP 1º a GP 5º
    colunas_gp_pi = ['GP P/I 1º', 'GP P/I 2º', 'GP P/I 3º', 'GP P/I 4º', 'GP P/I 5º']
    for coluna_d_pi, coluna_gp_pi in zip(colunas_d, colunas_gp_pi):
        dados[coluna_gp_pi] = dados[coluna_d_pi].apply(lambda x: next((grupo for grupo, info in tabela_grupos.items() if x in info['dezenas']), None))

    # Mapear os valores dos grupos para os nomes dos grupos e preencher as colunas BICHO 1º a BICHO 5º
    colunas_bicho = ['BICHO 1º', 'BICHO 2º', 'BICHO 3º', 'BICHO 4º', 'BICHO 5º']
    for coluna_gp_pi, coluna_bicho in zip(colunas_gp_pi, colunas_bicho):
        dados[coluna_bicho] = dados[coluna_gp_pi].apply(lambda x: tabela_grupos[x]['grupo'] if x in tabela_grupos else None)

    # Criar as colunas P/I 1º, P/I 2º, P/I 3º, P/I 4º, P/I 5º com base na análise de paridade
    colunas_pi = ['P/I 1º', 'P/I 2º', 'P/I 3º', 'P/I 4º', 'P/I 5º']
    for coluna_s, coluna_pi in zip(colunas_s, colunas_pi):
        paridade = [''.join(['I' if d % 2 == 1 else 'P' for d in lista]) for lista in dados[coluna_s]]
        dados[coluna_pi] = paridade

    # Preencher as colunas D P/I 1º a D P/I 5º com base na análise de paridade das dezenas
    colunas_d_pi = ['D P/I 1º', 'D P/I 2º', 'D P/I 3º', 'D P/I 4º', 'D P/I 5º']
    for coluna_d, coluna_d_pi in zip(colunas_d, colunas_d_pi):
        paridade = [''.join(['P' if int(digit) % 2 == 0 else 'I' for digit in str(valor)]) for valor in dados[coluna_d]]
        dados[coluna_d_pi] = paridade

    # Criar as colunas MC 1º, MC 2º, MC 3º, MC 4º, MC 5º com as duas primeiras posições das listas em S 1º, S 2º, S 3º, S 4º, S 5º
    colunas_mc = ['MC 1º', 'MC 2º', 'MC 3º', 'MC 4º', 'MC 5º']
    for coluna_s, coluna_mc in zip(colunas_s, colunas_mc):
        dados[coluna_mc] = dados[coluna_s].apply(lambda x: f"{x[0]:01}{x[1]:01}")

    # Criar as colunas MC P/I 1º, MC P/I 2º, MC P/I 3º, MC P/I 4º, MC P/I 5º com base na análise de paridade das colunas MC 1º, MC 2º, MC 3º, MC 4º, MC 5º
    colunas_mc_pi = ['MC P/I 1º', 'MC P/I 2º', 'MC P/I 3º', 'MC P/I 4º', 'MC P/I 5º']
    for coluna_mc, coluna_mc_pi in zip(colunas_mc, colunas_mc_pi):
        paridade_mc = [''.join(['P' if int(digit) % 2 == 0 else 'I' for digit in str(valor)]) for valor in dados[coluna_mc]]
        dados[coluna_mc_pi] = paridade_mc

    # Exibir as últimas 8 linhas atualizadas usando tabulate
    print(tabulate(dados.tail(8), headers='keys', tablefmt='pretty'))

    # Exportar para CSV com os novos dados
    dados.to_csv(os.path.join(caminho_pasta, 'BASE_DE_DADOS_2024_02_PROCESSADO.csv'), index=False)

else:
    print(f'O arquivo {caminho_arquivo} não foi encontrado.')
