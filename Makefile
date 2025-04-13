setup-environment: setup-tables install-uv test-sql
export TRAIN := ""

.PHONY: run-app
run-app:
	uv run python main $(TRAIN)

.PHONY: setup-tables
setup-tables:
	./tools/scripts/create_tables.sh
	./tools/scripts/comment_tables.sh
	./tools/scripts/insert_data.sh

.PHONY: install-uv
install-uv:
	uv pip install -e ".[dev]"

.PHONY: test-sql
test-sql:
	./tools/scripts/test_sql.sh

.PHONY: trino-shell
trino-shell:
	./tools/scripts/trino_shell.sh
