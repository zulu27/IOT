.PHONY: venv run_script clean

venv:
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt

run_script:
	./venv/bin/python3 set_redis_var.py

clean:
	rm -rf venv
