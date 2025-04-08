.PHONY: all create-environment process-data create-plots

all: create-environment process-data create-plots

create-environment:
	python -m venv .venv
	.venv\Scripts\activate
	pip install -r requirements.txt

process-data:
	python .\src\data.py

create-plots:
	python .\src\plots.py
