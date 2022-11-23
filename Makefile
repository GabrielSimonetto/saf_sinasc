THIS_PROJECT=saf_sinasc

install:
	poetry run pip install --upgrade pip
	poetry update -vv
	poetry install -vv
	poetry run ipython kernel install --user --name=$(THIS_PROJECT)