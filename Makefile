
# Install dependencies
setup:
	poetry update
	poetry install
	poetry config virtualenvs.in-project true
	pip install flake8
	pip install black

inspect:
	flake8 android_resources_checker
	black --check android_resources_checker

standard-inspection:
	poetry run android-resources-checker \
		--app-path=$(app-path)

## Deploy the current build to Pypi
deploy:
	poetry config pypi-token.pypi $(token)
	poetry build
	poetry publish