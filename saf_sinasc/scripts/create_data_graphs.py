"""
This module holds graphs related to data and sample analysis
"""

from saf_sinasc.feature_engineering import full_pipeline, basic_pipeline, load_negative_and_positive_df
from saf_sinasc.scripts.config import COMPILATIONS_PATH, DATA_GRAPHS_OUTPUT_PATH, SCRIPTS_OUTPUT_PATH
import tempfile
import subprocess
import time
import json
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import missingno as msno
import matplotlib
matplotlib.use('Agg')


PERCENTAGE = "2"
# TODO: bad name, should reflect not having positive entries
NEGATIVES_PATH = SCRIPTS_OUTPUT_PATH / \
    f"eda_sample_stratified_on_{PERCENTAGE}_percentage.csv"

assert SCRIPTS_OUTPUT_PATH.exists()
assert COMPILATIONS_PATH.exists()
assert DATA_GRAPHS_OUTPUT_PATH.exists()


# TODO: bad name, now used as input?
NEGATIVES_PATH = SCRIPTS_OUTPUT_PATH / \
    "eda_sample_stratified_on_2_percentage.csv"


def create_sample_with_nans():
    return basic_pipeline(NEGATIVES_PATH)


def create_sample_with_preprocessing_without_features():
    return full_pipeline(NEGATIVES_PATH, get_features=False, get_dummies_bool=False)


# TODO: use new changes
def missing_data_graph(df, title, filename):
    # fig = msno.bar(df)
    # # ok talvez eu escolha resolver isso de alguma forma
    # # lembrando que: eu soh to fazendo isso pq ta faltando espaço no relatorio
    # # eu posso achar outro grafico que funcione eu imagino

    # fig, ax = plt.subplots(figsize=(8, 6))
    # fig = msno.bar(df, ax=ax)

    fig = msno.bar(df)
    fig.set_title(title)
    fig_copy = fig.get_figure()
    fig_copy.savefig(DATA_GRAPHS_OUTPUT_PATH /
                     filename, bbox_inches='tight')
    plt.clf()


def corr_graph(df, num_columns=None):
    """Create a correlation heatmap

    If num_columns=None it's assumed you want all of them
    """

    from scipy.cluster import hierarchy

    num_columns = num_columns if num_columns else df.shape[1]

    corr_matrix = df.corr()
    selected_columns = corr_matrix['y'].abs().sort_values(
        ascending=False).head(num_columns).index

    corr_matrix = corr_matrix.loc[selected_columns, selected_columns]

    corr_clustered = hierarchy.linkage(corr_matrix, method='ward')
    corr_order = hierarchy.leaves_list(corr_clustered)
    corr_matrix_clustered = corr_matrix.iloc[corr_order, corr_order]

    title = f"Gráfico de Correlação Top {num_columns - 1}" if num_columns else f"Gráfico de Correlação"
    sns.heatmap(corr_matrix_clustered, cmap='coolwarm').set(
        title=title)
    plt.savefig(DATA_GRAPHS_OUTPUT_PATH / f'corr_graph_{num_columns}.png')
    plt.clf()


def create_all_data_graphs():
    start_time = time.time()

    df = load_negative_and_positive_df(NEGATIVES_PATH)
    missing_data_graph(df, 'Dados Faltantes', 'missing_data_semi_raw.png')

    df = create_sample_with_nans()
    missing_data_graph(df, 'Dados Faltantes', 'missing_data_clean.png')

    df = create_sample_with_preprocessing_without_features()
    corr_graph(df, 11)
    corr_graph(df, 21)
    # corr_graph(df)  # all
    # TODO: needs full sanitization (ANO has nan)

    end_time = time.time()

    print("Time elapsed: ", end_time - start_time, "seconds")

# def create_all_data_graphs():
#     start_time = time.time()

#     df = create_sample()
#     missing_data_graph(df)

#     end_time = time.time()

#     print("Time elapsed: ", end_time - start_time, "seconds")


if __name__ == '__main__':
    create_all_data_graphs()
