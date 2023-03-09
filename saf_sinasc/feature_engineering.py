import pandas as pd

from saf_sinasc.config import compilations_path

# Is there a convention name for this?


def full_pipeline(sample_path):
    """ full_pipeline

    pre_process_enrich_columns targets categorical columns
    preprocess_imputation targets numerical columns
    """

    return (
        load_negative_and_positive_df(sample_path)
        .pipe(drop_columns)
        .pipe(ensure_dtypes)
        .pipe(pre_process_enrich_columns)
        .pipe(preprocess_imputation)
        .pipe(feature_engineering)
        .pipe(get_dummies)
    )


def load_negative_and_positive_df(neutral_path):
    # TODO: hmm parameterizing neutral_path maybe implies parameterizing positives_path aswell.
    # neutral_path = compilations_path/"shuf_5x_01.csv"

    # Even more ghosts, at this point who knows if the neutral sample has the same origin as positives path
    positives_path = compilations_path / \
        "only_positives_for_q86_and_q870_between_2010_and_2019.csv"

    # # TODO
    # assert False, "Descobrindo como diabo coercionar isso em tempo de leitura"
    # # https://stackoverflow.com/questions/60553469/pandas-coerce-errors-while-reading-csv
    #
    # # fixed currently by ensure_dtypes()
    neutral_df = pd.read_csv(neutral_path)
    positives_df = pd.read_csv(positives_path)

    neutral_df['y'] = 0
    positives_df['y'] = 1

    print(
        f"positives_df.shape: {positives_df.shape}\n",
        f"neutral_df.shape: {neutral_df.shape}"
    )

    return pd.concat([positives_df, neutral_df])


# TODO: check all other columns
def ensure_dtypes(df):
    df["CODUFNATU"] = pd.to_numeric(df["CODUFNATU"], errors="coerce")

    return df


def treat_nan_and_map_values(df, col, col_map, nan_cat=9.0):
    return df.assign(**{col: lambda df: pd.to_numeric(df[col]).fillna(nan_cat).map(col_map)})


def enrich_LONASC(df):
    col = "LOCNASC"
    nan_cat = 5.0
    LOCNASC_map = {
        1: "Hospital",
        2: "Outro Estab. Saúde",
        3: "Domicílio",
        4: "Outros",
        5: "Ignorado",
    }

    return treat_nan_and_map_values(df, col, LOCNASC_map, nan_cat)


def enrich_ESTCIVMAE(df):
    col = "ESTCIVMAE"
    nan_cat = 9.0
    ESTCIVMAE_map = {
        1: 'Solteiro',
        2: 'Casado',
        3: 'Viúvo',
        4: 'Separado Judic./Divorciado',
        5: 'União consensual',
        9: 'Ignorado',
    }

    return treat_nan_and_map_values(df, col, ESTCIVMAE_map, nan_cat)


def enrich_ESCMAE(df):
    col = "ESCMAE"
    nan_cat = 9.0
    ESCMAE_map = {
        1: "Nenhuma",
        2: "1 a 3 anos",
        3: "4 a 7 anos",
        4: "8 a 11 anos",
        5: "12 e mais",
        9: "Ignorado",
    }

    return treat_nan_and_map_values(df, col, ESCMAE_map, nan_cat)


def enrich_ESCMAEAGR1(df):
    col = "ESCMAEAGR1"
    nan_cat = 9.0
    ESCMAEAGR1_map = {
        0:  "Sem Escolaridade",
        1:  "Fundamental I Incompleto",
        2:  "Fundamental I Completo",
        3:  "Fundamental II Incompleto",
        4:  "Fundamental II Completo",
        5:  "Ensino Médio Incompleto",
        6:  "Ensino Médio Completo",
        7:  "Superior Incompleto",
        8:  "Superior Completo",
        9:  "Ignorado",
        10: "Fundamental I Incompleto ou Inespecífico",
        11: "Fundamental II Incompleto ou Inespecífico",
        12: "Ensino Médio Incompleto ou Inespecífico",
    }

    return treat_nan_and_map_values(df, col, ESCMAEAGR1_map, nan_cat)


def enrich_GESTACAO(df):
    col = "GESTACAO"
    nan_cat = 9.0
    GESTACAO_map = {
        1: "Menos de 22 semanas",
        2: "22 a 27 semanas",
        3: "28 a 31 semanas",
        4: "32 a 36 semanas",
        5: "37 a 41 semanas",
        6: "42 semanas e mais",
        9: "Ignorado",
    }

    return treat_nan_and_map_values(df, col, GESTACAO_map, nan_cat)


def enrich_GRAVIDEZ(df):
    col = "GRAVIDEZ"
    nan_cat = 9.0
    GRAVIDEZ_map = {
        9: "Ignorado",
        1: "Única",
        2: "Dupla",
        3: "Tripla ou mais",
    }

    return treat_nan_and_map_values(df, col, GRAVIDEZ_map, nan_cat)


def enrich_PARTO(df):
    col = "PARTO"
    nan_cat = 9.0
    PARTO_map = {
        9: "Ignorado",
        1: "Vaginal",
        2: "Cesáreo",
    }

    return treat_nan_and_map_values(df, col, PARTO_map, nan_cat)


def enrich_CONSULTAS(df):
    col = "CONSULTAS"
    nan_cat = 9.0
    CONSULTAS_map = {
        9: "Ignorado",
        1: "Nenhuma",
        2: "de 1 a 3",
        3: "de 4 a 6",
        4: "7 e mais",
    }

    return treat_nan_and_map_values(df, col, CONSULTAS_map, nan_cat)


def enrich_SEXO(df):
    col = "SEXO"
    nan_cat = 9.0
    SEXO_map = {
        0: "Ignorado",
        1: "Masculino",
        2: "Feminino",
        9: "Ignorado",
    }

    # It's better to convert to numeric just to be type safe
    df = df.assign(**{
        "SEXO": lambda df: pd.to_numeric(df["SEXO"].replace({"M": 1, "F": 2}), errors='coerce')
    }
    )

    return treat_nan_and_map_values(df, col, SEXO_map, nan_cat)


def enrich_RACACOR(df):
    col = "RACACOR"
    nan_cat = 9.0
    RACACOR_map = {
        1: "Branca",
        2: "Preta",
        3: "Amarela",
        4: "Parda",
        5: "Indígena",
        9: "Ignorado",
    }

    return treat_nan_and_map_values(df, col, RACACOR_map, nan_cat)


def enrich_RACACORMAE(df):
    col = "RACACORMAE"
    nan_cat = 9.0
    RACACORMAE_map = {
        1: "Branca",
        2: "Preta",
        3: "Amarela",
        4: "Parda",
        5: "Indígena",
        9: "Ignorado",
    }

    return treat_nan_and_map_values(df, col, RACACORMAE_map, nan_cat)


def enrich_STTRABPART(df):
    col = "STTRABPART"
    nan_cat = 9.0
    STTRABPART_map = {
        1: "Sim",
        2: "Não",
        3: "Não se aplica",
        9: "Ignorado",
    }

    return treat_nan_and_map_values(df, col, STTRABPART_map, nan_cat)


def enrich_STCESPARTO(df):
    col = "STCESPARTO"
    nan_cat = 9.0
    STCESPARTO_map = {
        1: "Sim",
        2: "Não",
        3: "Não se aplica",
        9: "Ignorado",
    }

    return treat_nan_and_map_values(df, col, STCESPARTO_map, nan_cat)


def enrich_STDNEPIDEM(df):
    col = "STDNEPIDEM"
    nan_cat = 9.0
    STDNEPIDEM_map = {
        0: "Sim",
        1: "Nao",
        9: "Ignorado",
    }

    return treat_nan_and_map_values(df, col, STDNEPIDEM_map, nan_cat)


def enrich_STDNNOVA(df):
    col = "STDNNOVA"
    nan_cat = 9.0
    STDNNOVA_map = {
        0: "Sim",
        1: "Nao",
        9: "Ignorado",
    }

    return treat_nan_and_map_values(df, col, STDNNOVA_map, nan_cat)


def enrich_TPMETESTIM(df):
    col = "TPMETESTIM"
    nan_cat = 9.0
    TPMETESTIM_map = {
        1: "Exame físico",
        2: "Outro método",
        9: "Ignorado",
    }

    return treat_nan_and_map_values(df, col, TPMETESTIM_map, nan_cat)


def enrich_TPAPRESENT(df):
    col = "TPAPRESENT"
    nan_cat = 9.0
    TPAPRESENT_map = {
        1: "Cefálico",
        2: "Pélvica ou podálica",
        3: "Transversa",
        9: "Ignorado",
    }

    return treat_nan_and_map_values(df, col, TPAPRESENT_map, nan_cat)


def enrich_TPNASCASSI(df):
    col = "TPNASCASSI"
    nan_cat = 9.0
    TPNASCASSI_map = {
        1: "Médico",
        2: "Enfermeira/obstetriz",
        3: "Parteira",
        4: "Outros",
        9: "Ignorado",
    }

    return treat_nan_and_map_values(df, col, TPNASCASSI_map, nan_cat)


def enrich_TPFUNCRESP(df):
    col = "TPFUNCRESP"
    nan_cat = 9.0
    TPFUNCRESP_map = {
        1: "Médico",
        2: "Enfermeiro",
        3: "Parteira",
        4: "Funcionário do cartório",
        5: "Outros",
        9: "Ignorado",
    }

    return treat_nan_and_map_values(df, col, TPFUNCRESP_map, nan_cat)


def enrich_TPDOCRESP(df):
    col = "TPDOCRESP"
    nan_cat = 9.0
    TPDOCRESP_map = {
        1: "CNES",
        2: "CRM",
        3: "COREN",
        4: "RG",
        5: "CPF",
    }

    return treat_nan_and_map_values(df, col, TPDOCRESP_map, nan_cat)


def enrich_TPROBSON(df):
    col = "TPROBSON"
    nan_cat = 11.0
    TPROBSON_map = {
        1: "1",
        2: "2",
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        7: "7",
        8: "8",
        9: "9",
        10: "10",
        11: "Ignorado",
    }

    return treat_nan_and_map_values(df, col, TPROBSON_map, nan_cat)


def pre_process_enrich_columns(df):
    """Targets categorical values"""
    return (
        df
        .pipe(enrich_LONASC)
        .pipe(enrich_ESTCIVMAE)
        .pipe(enrich_ESCMAE)
        .pipe(enrich_ESCMAEAGR1)
        .pipe(enrich_GRAVIDEZ)
        .pipe(enrich_GESTACAO)
        .pipe(enrich_PARTO)
        .pipe(enrich_CONSULTAS)
        .pipe(enrich_SEXO)
        .pipe(enrich_RACACOR)
        .pipe(enrich_RACACORMAE)
        .pipe(enrich_STTRABPART)
        .pipe(enrich_STCESPARTO)
        .pipe(enrich_STDNEPIDEM)
        .pipe(enrich_STDNNOVA)
        .pipe(enrich_TPMETESTIM)
        .pipe(enrich_TPAPRESENT)
        .pipe(enrich_TPNASCASSI)
        .pipe(enrich_TPFUNCRESP)
        .pipe(enrich_TPDOCRESP)
        .pipe(enrich_TPROBSON)
    )


def feature_engineering(df):
    def is_equal(df, col1, col2):
        return df.assign(**{f"is_equal_{col1}_and_{col2}":
                            lambda df: (df.CODMUNRES ==
                                        df.CODMUNNASC).astype(int)
                            })

    print(f"feature_engineering: df shape: {df.shape}")

    df = (df
          .pipe(is_equal, col1="CODMUNRES", col2="CODMUNNASC")
          .pipe(is_equal, col1="CODMUNRES", col2="CODMUNNATU")
          .pipe(is_equal, col1="CODMUNNASC", col2="CODMUNNATU")
          )

    # TODO: might make logging a responsability from the main function later
    print(f"feature_engineering: df shape: {df.shape}")

    return df


def preprocess_imputation(df):
    # Depends on: ver se eu vou precisar inputação mesmo,
    #     provavelmente vou dar uma chance pra XGBOOST eu acho
    # TODO: tem coisa aqui que precisa fazer direito
    #     https://www.youtube.com/watch?v=m_qKhnaYZlc

    # TODO: agora sim eu posso acertar o config e passar a lista toda aqui maybe?
    selection_list = [
        "CODESTAB",
        "CODMUNNASC",
        "IDADEMAE",  # TODO mudar
        "CODOCUPMAE",
        "QTDFILVIVO",
        "QTDFILMORT",
        "CODMUNRES",
        "CODMUNNATU",
        "APGAR1",  # TODO mudar
        "APGAR5",  # TODO mudar
        "PESO",  # TODO mudar
        "SERIESCMAE",
        "QTDGESTANT",
        "QTDPARTNOR",
        "QTDPARTCES",
        "IDADEPAI",
        "SEMAGESTAC",
        "CONSPRENAT",
        "MESPRENAT",
        "ESCMAE2010",  # acho que isso aqui devia ser categorico
        "CODUFNATU",
        "CODMUNCART",
    ]

    return df.fillna(df[selection_list].median())


def drop_columns(df):
    """
    Legenda:
    ND - Não estão na Documentação
    NAN - Muitos valores NAN
    CR(col) - Coluna Redundante com outra coluna (col)
    IND - Informação Não Definida
    IL - Informação Limitada:
            ex: coluna com só um valor,
              : coluna sem valor semantico (codigos de cartorio)

    RACACORN: ND, NAN
    RACACOR_RN: ND, NAN

    CODCART: IL
    NUMREGCART: IL
    DTREGCART: IL
    CODPAISRES: IL, NAN
    DTCADASTRO: IL
    NUMEROLOTE: IL

    DTRECEBIM: IL
    DIFDATA: IL
    DTRECORIG : IND
    DTRECORIGA: IND

    DTNASCMAE: CR(IDADEMAE)
    DTULTMENST: IL
    DTDECLARAC: IL

    PARIDADE: ND
    KOTELCHUCK: ND

    CODCRM: IL,
    ORIGEM: IL, ND,
    VERSAOSIS: IL

    # ambas criadas por nós
    ESTADO_DF: CR(ESTADO),
    ANO_DF: CR(ANO),

    # Menção honrosa de colunas que VAO ser removidas:
        "DTNASC", # como particionar? verao inverno primavera outono?
        "HORANASC",
            :
                da pra enriquecer elas depois,
                e nao tao eficiente


        "IDANOMAL", "CODANOMAL": Coluna relacionada a anomalias congênitas,
                        é considerada >bleeding info< nesse problema
                            (consertar com termo tecnico depois.)

                        até dá pra criar a feature de
                            TEM_OUTRA_ANOMALIA_CONGENITA
                            mas parece um adicional opcional

        "NATURALMAE": se a mae é do brasil ou estrangeira,
                        parece usar codigos diferentes para o brasil,
                        como se fosse uma regiao socioeconomica,
                        como ja usamos colunas geograficas como a de ESTADO,
                        considera-se essa coluna como reduntante por enquanto.

    # Menção honrosa de colunas que NAO VAO ser removidas:

        CODESTAB, CODMUNNASC: IL,
              ao usar uma estrategia de sampling,
              é sempre altamente subrepresentada,
              ainda assim... certos estabelecimentos vao ter alta incidencia
              talvez simplesmente por serem efetivos em diagnosticar SAF

              vai ser mantido só pra caso a gente use o dataset inteiro depois.
    """

    columns = [
        "RACACORN",
        "RACACOR_RN",
        "CODCART",
        "NUMREGCART",
        "DTREGCART",
        "CODPAISRES",
        "DTCADASTRO",
        "NUMEROLOTE",
        "DTRECEBIM",
        "DIFDATA",
        "DTRECORIG",
        "DTRECORIGA",
        "DTNASCMAE",
        "DTULTMENST",
        "DTDECLARAC",
        "PARIDADE",
        "KOTELCHUCK",
        "CODCRM",
        "ORIGEM",
        "DTNASC",
        "HORANASC",
        "VERSAOSIST",
        "IDANOMAL",
        "CODANOMAL",
        "NATURALMAE",
        # "CODMUNNATU", # might be uncommented later, but we need it for feature creation
        "ESTADO_DF",
        "ANO_DF",
    ]

    output = df.drop(
        columns=columns,
        errors="ignore"  # if a column does not exist keep removing the others
    )

    print(
        f"remove_columns: df columns: {df.shape[1]}\n",
        f"remove_columns: columns to drop: {len(columns)}\n",
        f"remove_columns: output columns: {output.shape[1]}",
    )

    return output


def get_dummies(df):

    ENRICH_CAT_COLUMNS = [
        "LOCNASC",
        "ESTCIVMAE",
        "ESCMAE",
        "ESCMAEAGR1",  # nao achado em algumas iterações?
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
        "TPROBSON",  # TODO ver aquele link la
        # https://www.arca.fiocruz.br/bitstream/icict/29751/2/CLASSIFICA%C3%87%C3%83O%20DE%20ROBSON.pdf
        "ESTADO",
    ]
    DUMMIES_LIST = ENRICH_CAT_COLUMNS

    return pd.get_dummies(df, columns=DUMMIES_LIST)


# TODO: abort one of either: (df.CODMUNRES == df.CODMUNNASC).value_counts()
# TODO: abort one of either: (df.CODMUNRES == df.CODMUNNATU).value_counts() ## NATURALMAE eh similar?

# TODO: check if all columns are met on the sum of the lists (no intersections aswell)

# TODO: how to deal with future different columns?
# TODO: clear all useless comments

# TODO: descobrir um jeito mais simples de documentar essas meta informações das colunas?
#        da pra ja ir escrevendo no artigo mesmo acho
