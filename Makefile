THIS_PROJECT=saf_sinasc

install:
	poetry run pip install --upgrade pip
	poetry update -vv
	poetry install -vv
	poetry run ipython kernel install --user --name=$(THIS_PROJECT)

run:
	poetry run python saf_sinasc/main.py

irun:
	poetry run ipython -i saf_sinasc/main.py

model_graphs:
	poetry run python saf_sinasc/scripts/create_model_graphs.py --data_version=$(data_version)

data_graphs:
	poetry run python saf_sinasc/scripts/create_data_graphs.py

missing_data_report:
	poetry run python saf_sinasc/scripts/create_missing_data_report.py

all_graphs: model_graphs data_graphs

express_models:
	poetry run python saf_sinasc/scripts/express_models.py

metrics_table:
	poetry run python create_report_metrics_tables.py

final_columns_table:
	poetry run python create_report_of_final_columns.py

latex_tables: metrics_table final_columns_table
	