import csv
from collections import defaultdict
from datetime import datetime


# Função para obter o dia da semana
def obter_dia_semana(data):
    dias_semana = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
    dia_semana_idx = datetime.strptime(data, '%d/%m/%Y').weekday()
    return dias_semana[dia_semana_idx]


# Função para obter o grupo de uma milhar
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
            return info["grupo"]
    return "Desconhecido"


# Função para analisar repetições
def analisar_repeticoes(caminho_arquivo, premio_escolhido):
    repeticoes_por_milhar = defaultdict(int)
    detalhes_concursos = defaultdict(lambda: defaultdict(list))

    try:
        with open(caminho_arquivo, 'r') as arquivo_csv:
            leitor_csv = csv.reader(arquivo_csv)
            cabecalho = next(leitor_csv)
            linhas_analisadas = 0

            for linha in leitor_csv:
                linhas_analisadas += 1
                numero_concurso = linha[0]
                data_sorteio = linha[1]
                premios = linha[2:]  # Ignorar as primeiras colunas
                premio = premios[premio_escolhido - 1]  # Índice base 0
                for i in range(0, len(premio), 4):
                    milhar = premio[i:i + 4]
                    grupo_dezena = obter_grupo_dezena(milhar[2:])
                    detalhes_concursos[milhar]['Concursos'].append({
                        'Concurso': numero_concurso,
                        'Data': data_sorteio,
                        'Dia da Semana': obter_dia_semana(data_sorteio)
                    })
                    detalhes_concursos[milhar]['Grupo'] = grupo_dezena
                    repeticoes_por_milhar[milhar] += 1

        print(f"Análise de repetições para o Prêmio {premio_escolhido}:\n")
        repeticoes_filtradas = {milhar: contador for milhar, contador in repeticoes_por_milhar.items() if contador >= 2}
        if repeticoes_filtradas:
            for milhar, contador in repeticoes_filtradas.items():
                detalhes = detalhes_concursos.get(milhar, {})
                if detalhes and 'Concursos' in detalhes:
                    print(f"Milhar: {milhar}, Grupo: {detalhes['Grupo']}, Repetições: {contador}")
                    for repeticao in detalhes['Concursos']:
                        print(f"  Concurso: {repeticao['Concurso']}")
                        print(f"  Data: {repeticao['Data']}, Dia da Semana: {repeticao['Dia da Semana']}")
                    print()  # Linha em branco entre diferentes milhares
        else:
            print("Não foram encontradas repetições com mais de uma aparição.")

        print(f"Total de linhas analisadas: {linhas_analisadas}")

    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho_arquivo}")


# Função para exibir o menu
def menu():
    print("Menu de Análise de Repetições")
    print("1. Prêmio 1")
    print("2. Prêmio 2")
    print("3. Prêmio 3")
    print("4. Prêmio 4")
    print("5. Prêmio 5")
    escolha = int(input("Escolha o número do prêmio para análise (1 a 5): "))
    if escolha in range(1, 6):
        return escolha
    else:
        print("Escolha inválida.")
        return None


# Função principal
def main():
    caminho_arquivo_original = '/home/henrique/Documentos/Projeto Análise de Dados/federal.csv'

    while True:
        premio_escolhido = menu()
        if premio_escolhido is None:
            break
        analisar_repeticoes(caminho_arquivo_original, premio_escolhido)
        continuar = input("Deseja continuar buscando repetições? (S/N): ")
        if continuar.lower() != 's':
            break


if __name__ == "__main__":
    main()
