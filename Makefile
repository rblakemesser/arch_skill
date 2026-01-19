.PHONY: install remote_install

install:
	mkdir -p ~/.codex/prompts
	cp prompts/*.md ~/.codex/prompts/
	mkdir -p ~/.codex/templates/arch_skill
	cp templates/*.html ~/.codex/templates/arch_skill/

remote_install:
	@if [ -z "$(HOST)" ]; then echo "HOST is required. Usage: make remote_install HOST=<user@host>"; exit 1; fi
	@mkdir -p ~/.codex/prompts
	@ssh $(HOST) "mkdir -p ~/.codex/prompts ~/.codex/templates/arch_skill"
	@for f in ~/.codex/prompts/arch-*.md; do \
		[ -e "$$f" ] || continue; \
		scp $$f $(HOST):~/.codex/prompts/; \
	done
	@for f in ~/.codex/prompts/maestro-*.md; do \
		[ -e "$$f" ] || continue; \
		scp $$f $(HOST):~/.codex/prompts/; \
	done
	@for f in ~/.codex/prompts/qa-*.md; do \
		[ -e "$$f" ] || continue; \
		scp $$f $(HOST):~/.codex/prompts/; \
	done
	@scp ~/.codex/templates/arch_skill/*.html $(HOST):~/.codex/templates/arch_skill/
