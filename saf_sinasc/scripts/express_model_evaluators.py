from saf_sinasc.models import ModelEvaluator
from saf_sinasc.config import EVALUATORS_PATH, METRICS
from saf_sinasc.scripts.config import (
    MODEL_GRAPHS_OUTPUT_PATH,
    NUM_OF_FEATURES_TO_DISPLAY,
)

assert EVALUATORS_PATH.exists()

DATA_VERSION = "1004"

assert EVALUATORS_PATH.joinpath(
    DATA_VERSION
).exists(), f"Invalid DATA_VERSION: {DATA_VERSION}"

evaluators = [
    ModelEvaluator.load(file)
    for file in EVALUATORS_PATH.joinpath(DATA_VERSION).glob("*.joblib")
]

# for metric in METRICS:
#     plot_from_result_metrics(DATA_VERSION, evaluators, metric, 'mean')
#     plot_from_result_metrics(DATA_VERSION, evaluators, metric, 'median')

for evaluator in evaluators:
    evaluator.print_all()
    print()
    evaluator.show_results()
    print()
    evaluator.aggregate_results()
    print()
