from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent.parent.joinpath("data")
RAW_PATH = DATA_PATH / "raw"
SCRIPTS_OUTPUT_PATH = DATA_PATH / "scripts"
COMPILATIONS_PATH = DATA_PATH/"compilations"

GRAPHS_OUTPUT_PATH = SCRIPTS_OUTPUT_PATH / "graphs"
