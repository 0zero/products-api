mypy:
	bin/run-mypy.sh

lint:  mypy _formatters _isort

_formatters:
	bin/run-black.sh && \
	bin/run-flake8.sh

_isort:
	poetry run isort . $(ISORT_ARGS)
	