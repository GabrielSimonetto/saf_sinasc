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
