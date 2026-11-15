
import time


## ANALISADOR DE TEMPO ##

TEMPOS = []


def iniciar_cronometro():
    return time.perf_counter()


def parar_cronometro(nome, inicio):
    segundos = time.perf_counter() - inicio
    TEMPOS.append((nome, segundos))


def mostrar_tempos():
    print("\n--- Tempo de execução ---")

    for nome, segundos in TEMPOS:
        print(f"{nome}: {segundos:.4f} s")


## LEITURA E LIMPEZA ##

ARQUIVO_CSV = "dados_medio.csv"
CATEGORIAS = ["A", "B", "C"]
Registro = dict


def validar(linha):
    campos = [c.strip() for c in linha.split(",")]

    if len(campos) != 6:
        return None, "numero de colunas incorreto"

    if "" in campos:
        return None, "valor ausente"

    try:
        registro = {
            "id": int(campos[0]),
            "nome": campos[1],
            "categoria": campos[2],
            "idade": int(campos[3]),
            "nota": float(campos[4]),
            "tempo_min": float(campos[5]),
        }

    except ValueError:
        return None, "tipo invalido"

    if registro["categoria"] not in CATEGORIAS:
        return None, "categoria invalida"

    if not 0 <= registro["id"]:
        return None, "id fora da faixa"

    if not 0 <= registro["idade"] <= 120:
        return None, "idade fora da faixa"

    if not 0 <= registro["nota"] <= 10:
        return None, "nota fora da faixa"

    if registro["tempo_min"] <= 0:
        return None, "tempo fora da faixa"

    return registro, None


def ler_linhas(caminho=ARQUIVO_CSV):
    linhas = []

    with open(caminho, encoding="utf-8-sig") as arquivo:
        cabecalho = next(arquivo, None)

        if cabecalho is None:
            return linhas

        #arquivo vazio retorna none

        for numero, linha in enumerate(arquivo, start=2):
            if not linha.strip():
                continue

            linhas.append((numero, linha.strip()))

    return linhas


def limpar(linhas):
    validos, invalidos = [], []
    ids_vistos = set()

    for numero, linha in linhas:
        registro, motivo = validar(linha)

        if registro and registro["id"] in ids_vistos:
            registro, motivo = None, "id duplicado"

        if registro:
            ids_vistos.add(registro["id"])
            validos.append(registro)

        else:
            invalidos.append((numero, linha, motivo))

    return validos, invalidos


## FILTROS ##

FILTROS = {
    "id": [None, None],
    "nome": None,
    "categoria": [],
    "idade": [None, None],
    "nota": [None, None],
    "tempo_min": [None, None],
}

CAMPOS_NUMERICOS = [
    "id",
    "idade",
    "nota",
    "tempo_min",
]


def filtrar_intervalo(registros, campo, intervalo):
    minimo, maximo = intervalo

    resultado = []

    for registro in registros:
        valor = registro[campo]

        if minimo is not None and valor < minimo:
            continue

        if maximo is not None and valor > maximo:
            continue

        resultado.append(registro)

    return resultado


def filtrar_texto(registros, campo, texto):
    if not texto:
        return registros

    texto = texto.strip().lower()

    return [
        registro for registro in registros
        if texto in str(registro[campo]).lower()
    ]


def filtrar_lista(registros, campo, valores):
    if not valores:
        return registros

    return [
        registro for registro in registros
        if registro[campo] in valores
    ]


def aplicar_filtros(registros, filtros):
    resultado = registros

    for campo, valor in filtros.items():

        if campo in CAMPOS_NUMERICOS:
            resultado = filtrar_intervalo(
                resultado, campo, valor
            )

        elif campo == "nome":
            resultado = filtrar_texto(
                resultado, campo, valor
            )

        elif campo == "categoria":
            resultado = filtrar_lista(
                resultado, campo, valor
            )

    return resultado


def mostrar_filtros(filtros):
    print("Filtros ativos:")

    ativos = 0

    for campo, valor in filtros.items():

        if valor is not None and valor != [None, None] and valor != []:
            print(f"  {campo}: {valor}")
            ativos += 1

    if ativos == 0:
        print("  (nenhum)")


## CÁLCULO ##

CAMPOS_ESTATISTICOS = [
    "idade",
    "nota",
    "tempo_min",
]


def calcular_medidas(registros, campo):
    if not registros:
        return None

    valores = [r[campo] for r in registros]
    n = len(valores)

    # 1. Média
    media = sum(valores) / n

    # 2. Mediana
    ordenados = sorted(valores)
    meio = n // 2

    if n % 2 == 1:
        mediana = ordenados[meio]

    else:
        mediana = (
            ordenados[meio - 1] + ordenados[meio]
        ) / 2

    # 3. Moda
    frequencias = {}

    for v in valores:
        frequencias[v] = frequencias.get(v, 0) + 1

    maior_freq = max(frequencias.values())

    moda = sorted([
        v for v, freq in frequencias.items()
        if freq == maior_freq
    ])

    return {
        "media": round(media, 2),
        "mediana": round(mediana, 2),
        "moda": moda,
    }


## SAÍDA ##

LIMITE_EXIBICAO = 10

CAMPOS_EXIBIDOS = [
    "id",
    "nome",
    "categoria",
    "idade",
    "nota",
    "tempo_min",
]

CAMPOS_DISPONIVEIS = [
    "id",
    "nome",
    "categoria",
    "idade",
    "nota",
    "tempo_min",
]


def mostrar_registros(registros, campos, limite=LIMITE_EXIBICAO):

    for campo in campos:
        if campo not in CAMPOS_DISPONIVEIS:
            raise ValueError(f"campo inexistente: {campo}")

    total = len(registros)

    if total == 0:
        print("  (nenhum registro)")
        return

    for registro in registros[:limite]:

        partes = [
            f"{campo}: {registro[campo]}"
            for campo in campos
        ]

        print("  " + " | ".join(partes))

    restantes = total - limite

    if restantes > 0:
        print(f"  ... e mais {restantes}")


## SAÍDA PRINCIPAL ##

if __name__ == "__main__":

    TEMPOS.clear()

    inicio_total = iniciar_cronometro()

    # 1. Leitura
    inicio = iniciar_cronometro()

    try:
        linhas = ler_linhas(ARQUIVO_CSV)
    except FileNotFoundError:
        print(f"Erro: arquivo '{ARQUIVO_CSV}' nao encontrado.")
        raise SystemExit(1)

    parar_cronometro("ler_linhas", inicio)

    if not linhas:
        print(f"Aviso: '{ARQUIVO_CSV}' nao tem registros.")
        raise SystemExit(0)

    # 2. Limpeza
    inicio = iniciar_cronometro()

    validos, invalidos = limpar(linhas)

    parar_cronometro("limpar", inicio)

    print(f"Arquivo: {ARQUIVO_CSV}")
    print(f"{len(validos)} validos | {len(invalidos)} invalidos")

    # 3. Transformação
    inicio = iniciar_cronometro()

    filtrados = aplicar_filtros(validos, FILTROS)

    parar_cronometro("aplicar_filtros", inicio)

    print()
    mostrar_filtros(FILTROS)

    print(f"\n{len(filtrados)} registros passaram nos filtros")

    mostrar_registros(
        filtrados,
        CAMPOS_EXIBIDOS,
        LIMITE_EXIBICAO
    )

    # 4. Cálculo
    print("\n--- Medidas da Turma (Registros Válidos) ---")

    for campo in CAMPOS_ESTATISTICOS:

        inicio = iniciar_cronometro()

        medidas = calcular_medidas(validos, campo)

        parar_cronometro(
            f"calcular_medidas({campo})",
            inicio
        )

        if medidas:
            print(
                f"{campo.capitalize()}: "
                f"Média = {medidas['media']} | "
                f"Mediana = {medidas['mediana']} | "
                f"Moda = {medidas['moda']}"
            )

    # 5. Finalização
    parar_cronometro("programa inteiro", inicio_total)

    mostrar_tempos()
