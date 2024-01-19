import csv
from datetime import datetime


def converter_numero(numero):
    return "I" if int(numero) % 2 != 0 else "P"


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
                    numeros_convertidos = ''.join([converter_numero(digito) for digito in ajustar_resultado(premio)])
                    concurso["premios"].append(numeros_convertidos)

                dados_ordenados.append(concurso)

            # Ordena os dados cronologicamente
            dados_ordenados.sort(key=lambda x: x["data"])

            for concurso in dados_ordenados:
                linha_convertida = [concurso["numero"], concurso["data"].strftime("%d/%m/%Y")]
                linha_convertida.extend(concurso["premios"])
                dados_conversao.append(linha_convertida)

            for linha in dados_conversao:
                print(','.join(linha))

            # Pergunta ao usuário se deseja salvar a conversão em um novo arquivo CSV
            resposta = input("Deseja salvar a conversão em um novo arquivo CSV? (S/N): ")
            if resposta.upper() == "S":
                nome_arquivo_saida = '/home/henrique/Documentos/Projeto Análise de Dados/conversao_p_i.csv'
                with open(nome_arquivo_saida, 'w', newline='') as arquivo_saida:
                    escritor_csv = csv.writer(arquivo_saida)
                    for linha in dados_conversao:
                        escritor_csv.writerow(linha)
                print(f"Arquivo '{nome_arquivo_saida}' foi criado com sucesso.")

    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho_arquivo_original}")


# Chama a função para exibir a conversão
exibir_conversao()
