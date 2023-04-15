from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent.parent.joinpath("data")
RAW_PATH = DATA_PATH / "raw"
SCRIPTS_OUTPUT_PATH = DATA_PATH / "scripts"
COMPILATIONS_PATH = DATA_PATH/"compilations"
BY_STATE_PATH = COMPILATIONS_PATH/"by_state"

GRAPHS_OUTPUT_PATH = SCRIPTS_OUTPUT_PATH / "graphs"

DATA_GRAPHS_OUTPUT_PATH = GRAPHS_OUTPUT_PATH / "data_graphs"
MODEL_GRAPHS_OUTPUT_PATH = GRAPHS_OUTPUT_PATH / "model_graphs"

MODEL_GRAPHS_OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

NUM_OF_FEATURES_TO_DISPLAY = 10
