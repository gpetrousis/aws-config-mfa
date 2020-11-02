venv:
	test -d .venv || python3 -m venv .venv

install: venv
	. .venv/bin/activate && pip install -r requirements.txt

dev_install: venv
	. .venv/bin/activate && pip install -r requirements.dev.txt

test: dev_install
	pytest

clean:
	rm -rf ./.venv