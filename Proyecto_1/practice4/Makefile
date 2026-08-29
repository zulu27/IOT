.PHONY: venv run clean

venv:
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt

run:
	./venv/bin/python3 consume.py

clean:
	rm -rf venv
