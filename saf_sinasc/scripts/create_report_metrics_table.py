from saf_sinasc.scripts.config import MODEL_GRAPHS_OUTPUT_PATH, NUM_OF_FEATURES_TO_DISPLAY
from saf_sinasc.config import EVALUATORS_PATH, METRICS
from saf_sinasc.models import ModelEvaluator


def generate_table_header():
    header = """
% TODO a gente pode considerar lidar com mediana e stddev tbm
\\begin{table}[htbp]
    \centering
    \\begin{tabular}{|c|c|c|c|}
        \hline
        \\textbf{Modelo} & \\textbf{Hiperparâmetros} & \\textbf{Média F1} & \\textbf{Média ROC\_AUC} \\
        \hline
"""
    return header


def generate_table_closing():
    closing = """
        \hline
    \end{tabular}
    \caption{Tabela de Resultados}
    \label{tab:resultados}
\end{table}
"""
    return closing


def generate_tex_table(evaluators):
    table_content = generate_table_header()

    for evaluator in evaluators:
        # \\textbf{Modelo} & \\textbf{Hiperparâmetros} & \\textbf{Média F1} & \\textbf{Média ROC\_AUC} \\
        table_content += (
            "\t\t"
            + f"""{evaluator.name} & {evaluator.model} & {evaluator.get_agg("f1", "mean")} & {evaluator.get_agg("roc_auc", "mean")}"""
            + " \\\\\n"
        )

    table_content += generate_table_closing()

    return table_content


assert EVALUATORS_PATH.exists()

DATA_VERSION = '1000'

assert EVALUATORS_PATH.joinpath(
    DATA_VERSION).exists(), f"Invalid DATA_VERSION: {DATA_VERSION}"

evaluators = [ModelEvaluator.load(file) for file in EVALUATORS_PATH.joinpath(
    DATA_VERSION).glob("*.joblib")]

generated_table = generate_tex_table(evaluators)

with open("create_report_metrics_tables.txt", 'w') as f:
    f.write(generated_table)

# remember to run this repassing to create_report_metrics_tables_permanent.txt
# when needed
print(generated_table)
