from pathlib import Path

# TODO: uppercase all the paths
# TODO: I need to inherit these in the scripts folder maybe

DATAPATH = Path(__file__).resolve().parent.parent.joinpath("data")
compilations_path = DATAPATH/"compilations"
EVALUATORS_PATH = DATAPATH/"evaluators"
sample_lists_path = compilations_path/"sample_lists"  # TODO: Deprecated?
SAMPLES_PATH = compilations_path/"samples"  # TODO: make everyone uppercase?
by_state_path = compilations_path/"by_state"

METRICS = ["f1", "roc_auc", "roc_curve"]

# ESQUECE USAR ESSAS LISTAS NO CODIGO POR ENQUANTO
#    Provavelmente eh mais saudavel eu criar elas conforme eu vejo
#     o que acontece no codigo.
#     deixa isso aqui soh como documentação por enquanto
#  inclusive
#    mesmo na epoca que eu tava trabalhando,
#    eu ja nao tinha mais gostado do nome das classes
#    pega papel e caneta e desenha todas as divisorias que vc vai precisar aqui, se precisar

# pq isso tem esse nome?
NON_ENRICH_COLUMNS = [
    "CODESTAB",
    "CODMUNNASC",
    "CODMUNRES",
    "CODMUNCART",
    "CODUFNATU",
    "ESTADO",
    "LOCNASC",
    "CODOCUPMAE",  # create "other" for bottom 10%
]

ENRICH_CAT_COLUMNS = [
    "LOCNASC",
    "ESTCIVMAE",
    "ESCMAE",
    # "ESCMAEAGR1" # nao achado em algumas iterações?
    "GESTACAO",
    "GRAVIDEZ",
    "PARTO",
    "CONSULTAS",
    "SEXO",
    "RACACOR",
    "RACACORMAE",
    "STTRABPART",
    "STCESPARTO",
    "STDNEPIDEM",
    "STDNNOVA",
    "TPMETESTIM",
    "TPAPRESENT",
    "TPNASCASSI",
    "TPFUNCRESP",
    "TPDOCRESP",
    "TPROBSON",  # ver aquele link la
    # https://www.arca.fiocruz.br/bitstream/icict/29751/2/CLASSIFICA%C3%87%C3%83O%20DE%20ROBSON.pdf
]

# continuous significa tanto:
#     ordinal,
#     como... um milhao de valores floats -.-

# tenho que ver oqq eu queria com essa separação, idk
# acho que eu soh tinha que sair fazendo no braço,
# ao inves de classificando tudo assim.
CONTINUOUS_COLUMNS = [
    # true continuous
    "IDADEMAE",
    "IDADEPAI",
    "PESO",

    # ordinal
    "APGAR1",
    "APGAR5",
    "SERIESCMAE",
    "ESCMAE2010",
    "SEMAGESTAC",
    "CONSPRENAT",
    "MESPRENAT",
]

DISCRETE_COLUMNS = [
    "QTDFILVIVO",
    "QTDFILMORT",
    "QTDGESTANT",
    "QTDPARTNOR",
    "QTDPARTCES",
    "ANO",  # nao sei se eu quero indicar espectro?
]

# # SERIESCMAE --> "serie da mae" (tipo do ensino fundamental?)
# esperando pra ver se tem uma coluna de escolaridade melhor
#     R: tem: eh a ESCMAE2010
# # ESCMAEAGR1 --> tem que aglutinar com o outro ESCMAE e o outro outro SERIEC MAE

# quer saber eu lido com aquilo depois,
# por enquanto só classifica mesmo.

# # devia ter deixado aqui as que eu to incerto e fui enfiando no drop -.-
# "SERIESCMAE", # checar em relação a outra coluna la qq acontece (tem um comentario no notebook)

# creating now the see later cols: (incomplete, see all columns)
# "SERIESCMAE", # checar em relação a outra coluna la qq acontece (tem um comentario no notebook)

CATEGORIC_COLUMNS = [
    *NON_ENRICH_COLUMNS,
    *ENRICH_CAT_COLUMNS
]

# se eu nao encontrar uma categoria pra cada
# NAN value em cada categoria,
# eu posso inventar um padrao de precfixo de nome?

NUMERIC_COLUMNS = [
    *CONTINUOUS_COLUMNS,
    *DISCRETE_COLUMNS,  # puts mas discrete tem intersecção com categoric.
    # se pah eu explodo essa lsita de NUMERIC.
]

TARGET_COLUMN = ["y"]

ALL_COLUMNS = [*CATEGORIC_COLUMNS, *NUMERIC_COLUMNS, *TARGET_COLUMN]
