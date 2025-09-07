.PHONY: bootstrap eval24 decide

bootstrap:
	pip install -r requirements.txt >/dev/null

eval24:
	python -m evaluation.runner

decide:
	python -m evaluation.selector
