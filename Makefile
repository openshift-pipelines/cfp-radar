all:
	@uv run cfp-radar collect

html:
	@uv run cfp-radar generate
