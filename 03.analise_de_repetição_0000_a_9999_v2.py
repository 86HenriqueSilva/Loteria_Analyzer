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

# Função para analisar repetições entre os 1º ao 5º prêmios
def analisar_repeticoes_entre_premios(caminho_arquivo, todas_repeticoes_por_milhar, todas_detalhes_concursos):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo_csv:
            leitor_csv = csv.reader(arquivo_csv)
            cabecalho = next(leitor_csv)
            linhas_analisadas = 0

            for linha in leitor_csv:
                linhas_analisadas += 1
                numero_concurso, data_sorteio, *premios = linha
                for premio_escolhido in range(1, 6):  # Analisar os 5 prêmios
                    premio = premios[premio_escolhido - 1] if premio_escolhido <= len(premios) else None
                    if premio:
                        for i in range(0, len(premio), 4):
                            milhar = premio[i:i + 4]
                            grupo_dezena = obter_grupo_dezena(milhar[2:])
                            todas_detalhes_concursos[milhar]['Concursos'].append({
                                'Concurso': numero_concurso,
                                'Data': data_sorteio,
                                'Dia da Semana': obter_dia_semana(data_sorteio)
                            })
                            todas_detalhes_concursos[milhar]['Grupo'] = grupo_dezena
                            todas_repeticoes_por_milhar[milhar] += 1

        print("Análise de repetições entre os 1º ao 5º prêmios:\n")
        repeticoes_filtradas = {milhar: contador for milhar, contador in todas_repeticoes_por_milhar.items() if contador >= 2}
        if repeticoes_filtradas:
            for milhar, contador in repeticoes_filtradas.items():
                detalhes = todas_detalhes_concursos.get(milhar, {})
                if detalhes and 'Concursos' in detalhes:
                    print(f"Milhar: {milhar}, Grupo: {detalhes['Grupo']}, Repetições: {contador}")
                    for repeticao in detalhes['Concursos']:
                        print(f"  Concurso: {repeticao['Concurso']}")
                        print(f"  Data: {repeticao['Data']}, Dia da Semana: {repeticao['Dia da Semana']}")
                    print()  # Linha em branco entre diferentes milhares

            opcao = input("Deseja visualizar apenas as milhares em duplicidade? (S/N): ").strip().lower()
            if opcao == 's':
                milhares_em_duplicidade = [milhar for milhar, contador in repeticoes_filtradas.items() if contador > 2]
                if milhares_em_duplicidade:
                    print("Milhares em duplicidade:")
                    for i, milhar in enumerate(milhares_em_duplicidade, start=1):
                        print(milhar, end=' ')
                        if i % 10 == 0:
                            print()  # Iniciar nova linha após 10 milhares
                    print()  # Linha em branco no final
                    print(f"Total de milhares em duplicidade: {len(milhares_em_duplicidade)}")
                else:
                    print("Não foram encontradas milhares em duplicidade.")
        else:
            print("Não foram encontradas repetições com mais de uma aparição.")

        print(f"Total de linhas analisadas: {linhas_analisadas}")

    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho_arquivo}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {str(e)}")

# Função para analisar repetições
def analisar_repeticoes(caminho_arquivo, premio_escolhido, todas_repeticoes_por_milhar, todas_detalhes_concursos):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo_csv:
            leitor_csv = csv.reader(arquivo_csv)
            cabecalho = next(leitor_csv)
            linhas_analisadas = 0

            for linha in leitor_csv:
                linhas_analisadas += 1
                numero_concurso, data_sorteio, *premios = linha
                premio = premios[premio_escolhido - 1] if premio_escolhido <= len(premios) else None
                if premio:
                    for i in range(0, len(premio), 4):
                        milhar = premio[i:i + 4]
                        grupo_dezena = obter_grupo_dezena(milhar[2:])
                        todas_detalhes_concursos[milhar]['Concursos'].append({
                            'Concurso': numero_concurso,
                            'Data': data_sorteio,
                            'Dia da Semana': obter_dia_semana(data_sorteio)
                        })
                        todas_detalhes_concursos[milhar]['Grupo'] = grupo_dezena
                        todas_repeticoes_por_milhar[milhar] += 1

        print(f"Análise de repetições para o Prêmio {premio_escolhido}:\n")
        repeticoes_filtradas = {milhar: contador for milhar, contador in todas_repeticoes_por_milhar.items() if contador >= 2}
        if repeticoes_filtradas:
            for milhar, contador in repeticoes_filtradas.items():
                detalhes = todas_detalhes_concursos.get(milhar, {})
                if detalhes and 'Concursos' in detalhes:
                    print(f"Milhar: {milhar}, Grupo: {detalhes['Grupo']}, Repetições: {contador}")
                    for repeticao in detalhes['Concursos']:
                        print(f"  Concurso: {repeticao['Concurso']}")
                        print(f"  Data: {repeticao['Data']}, Dia da Semana: {repeticao['Dia da Semana']}")
                    print()  # Linha em branco entre diferentes milhares

            opcao = input("Deseja visualizar apenas as milhares em duplicidade? (S/N): ").strip().lower()
            if opcao == 's':
                milhares_em_duplicidade = [milhar for milhar, contador in repeticoes_filtradas.items() if contador > 2]
                if milhares_em_duplicidade:
                    print("Milhares em duplicidade:")
                    for i, milhar in enumerate(milhares_em_duplicidade, start=1):
                        print(milhar, end=' ')
                        if i % 10 == 0:
                            print()  # Iniciar nova linha após 10 milhares
                    print()  # Linha em branco no final
                    print(f"Total de milhares em duplicidade: {len(milhares_em_duplicidade)}")
                else:
                    print("Não foram encontradas milhares em duplicidade.")
        else:
            print("Não foram encontradas repetições com mais de uma aparição.")

        print(f"Total de linhas analisadas: {linhas_analisadas}")

    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho_arquivo}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {str(e)}")

# Função para exibir o menu
def menu():
    print("Menu de Análise de Repetições")
    print("1. Prêmio 1")
    print("2. Prêmio 2")
    print("3. Prêmio 3")
    print("4. Prêmio 4")
    print("5. Prêmio 5")
    print("6. Repetições entre os 1º ao 5º prêmios")
    print("q. Sair")
    escolha = input("Escolha o número do prêmio para análise (1 a 6) ou 'q' para sair: ").strip().lower()
    return escolha

# Função principal
def main():
    caminho_arquivo_original = "/home/henrique/Documentos/Projeto Análise de Dados/federal.csv"
    todas_repeticoes_por_milhar = defaultdict(int)
    todas_detalhes_concursos = defaultdict(lambda: {'Concursos': [], 'Grupo': ''})

    while True:
        escolha = menu()
        if escolha == 'q':
            break
        elif escolha.isdigit() and 1 <= int(escolha) <= 6:
            premio_escolhido = int(escolha)
            if premio_escolhido == 6:
                analisar_repeticoes_entre_premios(caminho_arquivo_original, todas_repeticoes_por_milhar, todas_detalhes_concursos)
            else:
                analisar_repeticoes(caminho_arquivo_original, premio_escolhido, todas_repeticoes_por_milhar, todas_detalhes_concursos)
        else:
            print("Escolha inválida. Por favor, escolha um número de 1 a 6 ou 'q' para sair.")

if __name__ == "__main__":
    main()
