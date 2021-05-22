LOCATIONS = cal_pal.py ./test/

check:
	black . && isort . && mypy $(LOCATIONS) --check-untyped-defs && python -m pytest

cov:
	coverage run -m pytest && coverage report && coverage html
