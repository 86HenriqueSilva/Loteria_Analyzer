import csv
from datetime import datetime
from collections import defaultdict

def obter_dia_semana(data):
    dias_semana = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
    dia_semana_idx = datetime.strptime(data, '%d/%m/%Y').weekday()
    return dias_semana[dia_semana_idx]

def obter_grupo_dezena(dezena):
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
    for grupo, info in tabela_grupos.items():
        if dezena in info["dezenas"]:
            return grupo, info["grupo"]
    return "Desconhecido", "Desconhecido"

def analisar_dezena_extracao(caminho_arquivo, dezena_escolhida, numero_extracao):
    contagem_dezena = defaultdict(int)
    detalhes_concursos = defaultdict(dict)

    with open(caminho_arquivo, 'r') as arquivo_csv:
        leitor_csv = csv.reader(arquivo_csv)
        cabecalho = next(leitor_csv)
        total_linhas_analisadas = 0

        for linha in leitor_csv:
            total_linhas_analisadas += 1
            numero_concurso = linha[0]
            data_sorteio = linha[1]
            detalhes_concursos[numero_concurso] = {
                'Data': data_sorteio,
                'Dia da Semana': obter_dia_semana(data_sorteio)
            }

            dezenas = linha[numero_extracao + 1]  # +1 para pular as colunas Nome e Data
            if dezena_escolhida in dezenas:
                grupo, nome_grupo = obter_grupo_dezena(dezena_escolhida)
                contagem_dezena[numero_concurso] += 1
                detalhes_concursos[numero_concurso]['Grupo'] = nome_grupo
                detalhes_concursos[numero_concurso]['Dezena'] = dezena_escolhida

    print(f"Resultados para a dezena {dezena_escolhida} na extração {numero_extracao}:\n")
    for numero_concurso, contagem in contagem_dezena.items():
        detalhes = detalhes_concursos[numero_concurso]
        print(f"  Concurso: {numero_concurso}")
        print(f"  Data: {detalhes['Data']}")
        print(f"  Dia da Semana: {detalhes['Dia da Semana']}")
        print(f"  Grupo: {detalhes['Grupo']}")
        print(f"  Número sorteado: {detalhes['Dezena']}\n")

    print(f"Total de concursos encontrados: {len(contagem_dezena)}")
    print(f"Total de linhas analisadas: {total_linhas_analisadas}")

def menu():
    print("Menu de Análise de Dezena por Extração")
    print("1. Analisar dezena em extração")
    print("2. Sair")
    escolha = int(input("Escolha uma opção: "))
    return escolha

def main():
    caminho_arquivo_original = '/home/henrique/Documentos/Projeto Análise de Dados/federal.csv'

    while True:
        escolha = menu()
        if escolha == 1:
            dezena_escolhida = input("Informe a dezena que deseja analisar: ")
            numero_extracao = int(input("Informe a extração de 1 a 5: "))
            analisar_dezena_extracao(caminho_arquivo_original, dezena_escolhida, numero_extracao)
        elif escolha == 2:
            break
        else:
            print("Opção inválida. Por favor, escolha novamente.")

if __name__ == "__main__":
    main()

#Concurso: 5729
# Data: 07/01/2023
# Dia da Semana: Sábado
# Grupo: URSO
# Número sorteado: 90
# melhorar exibindo a milhar do concurso