import csv
from collections import defaultdict
from datetime import datetime
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas

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


dias_semana = {
    "Monday": "Segunda-feira",
    "Tuesday": "Terça-feira",
    "Wednesday": "Quarta-feira",
    "Thursday": "Quinta-feira",
    "Friday": "Sexta-feira",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}
def exibir_dados():
    with open('dados.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)

def converter_data(data_str):
    return datetime.strptime(data_str, "%d/%m/%Y")

def contar_dezenas_unidades(extracao):
    contador_grupos = defaultdict(list)

    with open('dados.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            draw_date = converter_data(row[1])
            lista = eval(row[extracao])
            dezena_unidade = lista[2] + lista[3]
            concurso = row[0]

            for chave, valor in tabela_grupos.items():
                if dezena_unidade in valor["dezenas"]:
                    grupo = valor["grupo"]
                    contador_grupos[grupo].append((draw_date, concurso, row[2], dezena_unidade))
                    break

    contador_grupos = {grupo: sorted(registros, key=lambda x: x[0]) for grupo, registros in contador_grupos.items()}
    return contador_grupos

def calcular_frequencia_grupos(contador_grupos):
    frequencia_grupos = {}

    for grupo, registros in contador_grupos.items():
        frequencia_grupos[grupo] = len(registros)

    grupos_mais_sairam = sorted(frequencia_grupos.items(), key=lambda x: x[1], reverse=True)
    grupos_menos_sairam = sorted(frequencia_grupos.items(), key=lambda x: x[1])

    return grupos_mais_sairam, grupos_menos_sairam

def gerar_relatorio_pdf(grupos_mais_sairam, grupos_menos_sairam):
    pdf_filename = "/home/henrique/Documentos/RELATÓRIOS/relatorio.pdf"

    c = canvas.Canvas(pdf_filename, pagesize=landscape(letter))
    c.setFont("Helvetica", 12)

    c.drawString(100, 770, "Relatório de Análise de Dados")

    y = 720
    for grupo, quantidade in grupos_mais_sairam:
        c.drawString(100, y, f"Grupo {grupo}:")
        y -= 20
        for registro in contador[grupo]:
            draw_date, concurso, draw_time, dezena_unidade = registro
            day_of_week = dias_semana[draw_date.strftime("%A")]
            c.drawString(120, y, f"Concurso {concurso:4}, {draw_date.strftime('%d/%m/%Y'):12}, {day_of_week:13}, {draw_time:12}, {dezena_unidade:4}")
            y -= 15
        c.drawString(100, y, f"Quantidade {quantidade}")
        y -= 20
        c.drawString(100, y, "-" * 50)
        y -= 20

    # ... (mesmo padrão para os grupos que menos saíram)

    c.save()
    print(f"Relatório gerado: {pdf_filename}")

def menu():
    while True:
        print("Menu:")
        print("1. Extração 1º")
        print("2. Extração 2º")
        print("3. Extração 3º")
        print("4. Extração 4º")
        print("5. Extração 5º")
        print("0. Sair")
        escolha = input("Escolha a Extração para Análise de dados (0-5): ")

        if escolha in ["1", "2", "3", "4", "5"]:
            escolha = int(escolha)
            contador = contar_dezenas_unidades(escolha + 1)
            contador = dict(sorted(contador.items(), key=lambda x: x[0]))
            grupos_mais_sairam, grupos_menos_sairam = calcular_frequencia_grupos(contador)

            print("Grupos que mais saíram:")
            for grupo, quantidade in grupos_mais_sairam:
                print(f"{grupo}:")
                for registro in contador[grupo]:
                    draw_date, concurso, draw_time, dezena_unidade = registro
                    day_of_week = dias_semana[draw_date.strftime("%A")]
                    print(f"Concurso {concurso:4}, {draw_date.strftime('%d/%m/%Y'):12}, {day_of_week:13}, {draw_time:12}, {dezena_unidade:4}")
                print(f"Quantidade {quantidade}\n")

            print("Grupos que menos saíram:")
            for grupo, quantidade in grupos_menos_sairam:
                print(f"{grupo}:")
                for registro in contador[grupo]:
                    draw_date, concurso, draw_time, dezena_unidade = registro
                    day_of_week = dias_semana[draw_date.strftime("%A")]
                    print(f"Concurso {concurso:4}, {draw_date.strftime('%d/%m/%Y'):12}, {day_of_week:13}, {draw_time:12}, {dezena_unidade:4}")
                print(f"Quantidade {quantidade}\n")
        elif escolha == "0":
            break
        else:
            print("Opção inválida. Por favor, escolha novamente.")

if __name__ == "__main__":
    menu()

    # Após sair do loop do menu, pergunte se deseja salvar o relatório em PDF
    salvar_relatorio = input("Deseja salvar o relatório em PDF? (s/n): ")
    if salvar_relatorio.lower() == "s":
        gerar_relatorio_pdf(grupos_mais_sairam, grupos_menos_sairam)