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
caminho_pasta = '/home/henrique/Documentos/PROJETO 2024'
nome_arquivo = 'BASE_DE_DADOS_2024_02_PROCESSADO.csv'  # Nome do arquivo CSV
caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)

# Verificar se o arquivo existe antes de tentar ler
if os.path.exists(caminho_arquivo):
    # Use o método read_csv do Pandas para ler o arquivo CSV
    dados = pd.read_csv(caminho_arquivo)

    # Ajustar o formato da coluna de data
    dados['Data'] = pd.to_datetime(dados['Data'], format='%Y-%m-%d', errors='coerce').dt.date

    # Configurar local para português do Brasil
    locale = Locale('pt_BR')

    # Preencher a coluna "D/SEMAN" com o dia da semana em português
    dados['D/SEMAN'] = dados['Data'].apply(lambda x: format_date(x, 'EEEE', locale=locale) if pd.notnull(x) else '')

    # Exibir as últimas 8 linhas atualizadas usando tabulate
    print(tabulate(dados.tail(8), headers='keys', tablefmt='pretty'))

    # Exportar para CSV com os novos dados
    dados.to_csv(os.path.join(caminho_pasta, 'base.csv'), index=False)

else:
    print(f'O arquivo {caminho_arquivo} não foi encontrado.')
