def encontrar_grupo_animal(numero):
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

    dezena = numero[-2:]
    for grupo, info in tabela_grupos.items():
        if dezena in info["dezenas"]:
            return f"Grupo {grupo} - {info['grupo']} ({dezena})"

    return "Nenhum grupo encontrado para o número de dezena fornecido."


def gerar_numeros():
    numeros = []
    contagem_grupos = {}  # Dicionário para armazenar as contagens dos grupos
    total_pares = 0
    total_impares = 0

    # Receber entrada da milhar
    while True:
        milhar_input = input("Por favor, informe os dígitos atrasados na milhar (separados por vírgula): ")
        milhar_lista = milhar_input.split(',')
        if all(numero.isdigit() and 0 <= int(numero) <= 9 for numero in milhar_lista):
            milhar = [int(numero) for numero in milhar_lista]
            break
        else:
            print("Entrada inválida. Por favor, digite apenas números entre 0 e 9 separados por vírgula.")

    # Receber entrada da centena
    while True:
        centena_input = input("Por favor, informe os dígitos atrasados na centena (separados por vírgula): ")
        centena_lista = centena_input.split(',')
        if all(numero.isdigit() and 0 <= int(numero) <= 9 for numero in centena_lista):
            centena = [int(numero) for numero in centena_lista]
            break
        else:
            print("Entrada inválida. Por favor, digite apenas números entre 0 e 9 separados por vírgula.")

    # Receber entrada da dezena
    while True:
        dezena_input = input("Por favor, informe os dígitos atrasados na dezena (separados por vírgula): ")
        dezena_lista = dezena_input.split(',')
        if all(numero.isdigit() and 0 <= int(numero) <= 9 for numero in dezena_lista):
            dezena = [int(numero) for numero in dezena_lista]
            break
        else:
            print("Entrada inválida. Por favor, digite apenas números entre 0 e 9 separados por vírgula.")

    # Receber entrada da unidade
    while True:
        unidade_input = input("Por favor, informe os dígitos atrasados na unidade (separados por vírgula): ")
        unidade_lista = unidade_input.split(',')
        if all(numero.isdigit() and 0 <= int(numero) <= 9 for numero in unidade_lista):
            unidade = [int(numero) for numero in unidade_lista]
            break
        else:
            print("Entrada inválida. Por favor, digite apenas números entre 0 e 9 separados por vírgula.")

    for d1 in milhar:
        for d2 in centena:
            for d3 in dezena:
                for d4 in unidade:
                    numero = str(d1) + str(d2) + str(d3) + str(d4)
                    grupo_animal = encontrar_grupo_animal(str(d3) + str(d4))
                    numeros.append((numero, grupo_animal))

                    # Atualizar a contagem do grupo no dicionário
                    grupo = grupo_animal.split()[1]  # Extrair o número do grupo
                    contagem_grupos[grupo] = contagem_grupos.get(grupo, 0) + 1

                    # Atualizar a contagem de pares e ímpares
                    if int(d4) % 2 == 0:
                        total_pares += 1
                    else:
                        total_impares += 1

    # Imprimir os números e seus grupos correspondentes
    for numero, grupo_animal in numeros:
        print(f"{numero} - {grupo_animal}")

    # Imprimir a contagem de grupos
    print("\nContagem de grupos:")
    for grupo, contagem in contagem_grupos.items():
        print(f"Grupo {grupo}: {contagem}")

    # Imprimir a contagem de pares e ímpares
    print(f"\nTotal de números pares: {total_pares}")
    print(f"Total de números ímpares: {total_impares}")


gerar_numeros()
