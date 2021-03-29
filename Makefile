
# Install dependencies
setup:
	poetry update
	poetry install
	poetry config virtualenvs.in-project true
	pip install flake8
	pip install black

inspect:
	flake8 android-resources-checker
	black --check android-resources-checker

standard-inspection:
	poetry run android-resources-checker/main.py \
		--app-path=$(app-path)