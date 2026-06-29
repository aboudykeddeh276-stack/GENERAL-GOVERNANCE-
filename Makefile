.PHONY: install test build run package clean

install:
	python -m pip install -e .

test:
	pytest -q

build:
	python -m virtual_brain_pc.cli build --target local

run:
	python -m virtual_brain_pc.cli run --cycles 5

package:
	python -m build

clean:
	rm -rf dist build .pytest_cache *.egg-info src/*.egg-info
