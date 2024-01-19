import csv
from datetime import datetime

# Tabela de grupos e suas dezenas correspondentes
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

# Função para converter o número do prêmio em grupos
def converter_numero(numero):
    numero_terminacao = numero[-2:]  # Obtém os últimos dois dígitos do número
    for grupo, info in tabela_grupos.items():
        if numero_terminacao in info["dezenas"]:
            return grupo
    return "N/A"  # Caso a terminação não esteja na tabela

def ajustar_resultado(resultado):
    resultado = resultado.replace("mio", "Prêmio")
    return resultado.zfill(4)

def exibir_conversao():
    caminho_arquivo_original = '/home/henrique/Documentos/Projeto Análise de Dados/federal.csv'

    try:
        with open(caminho_arquivo_original, 'r') as arquivo_csv:
            leitor_csv = csv.reader(arquivo_csv)
            cabecalho = next(leitor_csv)

            dados_conversao = [cabecalho]
            dados_ordenados = []

            for linha in leitor_csv:
                concurso = {
                    "numero": linha[0],
                    "data": datetime.strptime(linha[1], "%d/%m/%Y"),
                    "premios": []
                }

                for premio in linha[2:]:
                    numero_convertido = converter_numero(premio)
                    concurso["premios"].append(numero_convertido)

                dados_ordenados.append(concurso)

            dados_ordenados.sort(key=lambda x: x["data"])

            for concurso in dados_ordenados:
                linha_convertida = [concurso["numero"], concurso["data"].strftime("%d/%m/%Y")]
                linha_convertida.extend(concurso["premios"])
                dados_conversao.append(linha_convertida)

            for linha in dados_conversao:
                print(','.join(linha))

            resposta = input("Deseja salvar a conversão em um novo arquivo CSV? (S/N): ")
            if resposta.upper() == "S":
                nome_arquivo_saida = '/home/henrique/Documentos/Projeto Análise de Dados/conversao_grupos.csv'
                with open(nome_arquivo_saida, 'w', newline='') as arquivo_saida:
                    escritor_csv = csv.writer(arquivo_saida)
                    for linha in dados_conversao:
                        escritor_csv.writerow(linha)
                print(f"Arquivo '{nome_arquivo_saida}' foi criado com sucesso.")

    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho_arquivo_original}")

# Chama a função para exibir a conversão
exibir_conversao()
