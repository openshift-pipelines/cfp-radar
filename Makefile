all:
	@uv run cfp-radar collect

html:
	@uv run cfp-radar generate

lint:
	@uvx ruff check

lint-fix:
	@uvx ruff check --fix

format:
	@uv format
