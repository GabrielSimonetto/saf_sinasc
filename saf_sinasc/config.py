from pathlib import Path

DATAPATH = Path(__file__).resolve().parent.parent.parent.parent.joinpath("notebooks/data")
compilations_path = DATAPATH/"compilations"
sample_lists_path = compilations_path/"sample_lists"
by_state_path = compilations_path/"by_state"
