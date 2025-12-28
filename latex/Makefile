# =============================================================================
# LaTeX Build Makefile
# =============================================================================
# Usage:
#   make              - Build all papers
#   make esl          - Build ESL paper
#   make clean        - Remove build artifacts
#   make distclean    - Remove all generated files including PDFs
#   make install-deps - Install LaTeX dependencies
# =============================================================================

# Directories
PAPERS_DIR = papers
OUTPUT_DIR = output

# LaTeX compiler settings
LATEX = pdflatex
LATEXMK = latexmk
LATEXMK_FLAGS = -pdf -interaction=nonstopmode -halt-on-error -output-directory=$(OUTPUT_DIR)
LATEX_FLAGS = -interaction=nonstopmode -halt-on-error -output-directory=$(OUTPUT_DIR)

# Papers
ESL_PAPER = $(PAPERS_DIR)/ESL_Paper_v12.tex

# Default target
.PHONY: all
all: esl

# Create output directory
$(OUTPUT_DIR):
	mkdir -p $(OUTPUT_DIR)

# Build ESL paper
.PHONY: esl
esl: $(OUTPUT_DIR)
	@echo "Building ESL Paper..."
	@if command -v latexmk >/dev/null 2>&1; then \
		cd $(PAPERS_DIR) && $(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error -output-directory=../$(OUTPUT_DIR) ESL_Paper_v12.tex; \
	else \
		cd $(PAPERS_DIR) && $(LATEX) $(LATEX_FLAGS) ESL_Paper_v12.tex && \
		$(LATEX) $(LATEX_FLAGS) ESL_Paper_v12.tex; \
	fi
	@echo "Done! Output: $(OUTPUT_DIR)/ESL_Paper_v12.pdf"

# Build with BibTeX support
.PHONY: esl-full
esl-full: $(OUTPUT_DIR)
	@echo "Building ESL Paper (full build with bibliography)..."
	cd $(PAPERS_DIR) && $(LATEX) $(LATEX_FLAGS) ESL_Paper_v12.tex
	cd $(PAPERS_DIR) && bibtex ../$(OUTPUT_DIR)/ESL_Paper_v12 || true
	cd $(PAPERS_DIR) && $(LATEX) $(LATEX_FLAGS) ESL_Paper_v12.tex
	cd $(PAPERS_DIR) && $(LATEX) $(LATEX_FLAGS) ESL_Paper_v12.tex
	@echo "Done! Output: $(OUTPUT_DIR)/ESL_Paper_v12.pdf"

# Watch for changes and rebuild (requires latexmk)
.PHONY: watch
watch: $(OUTPUT_DIR)
	@echo "Watching for changes..."
	cd $(PAPERS_DIR) && $(LATEXMK) -pvc -pdf -interaction=nonstopmode -output-directory=../$(OUTPUT_DIR) ESL_Paper_v12.tex

# Install LaTeX dependencies
.PHONY: install-deps
install-deps:
	@echo "Installing LaTeX dependencies..."
	./scripts/install-latex-packages.sh

# Check if LaTeX is installed
.PHONY: check
check:
	@echo "Checking LaTeX installation..."
	@command -v pdflatex >/dev/null 2>&1 && echo "pdflatex: OK" || echo "pdflatex: NOT FOUND"
	@command -v latexmk >/dev/null 2>&1 && echo "latexmk: OK" || echo "latexmk: NOT FOUND"
	@command -v biber >/dev/null 2>&1 && echo "biber: OK" || echo "biber: NOT FOUND"
	@command -v bibtex >/dev/null 2>&1 && echo "bibtex: OK" || echo "bibtex: NOT FOUND"

# Clean build artifacts
.PHONY: clean
clean:
	@echo "Cleaning build artifacts..."
	rm -f $(OUTPUT_DIR)/*.aux $(OUTPUT_DIR)/*.log $(OUTPUT_DIR)/*.out
	rm -f $(OUTPUT_DIR)/*.toc $(OUTPUT_DIR)/*.lof $(OUTPUT_DIR)/*.lot
	rm -f $(OUTPUT_DIR)/*.bbl $(OUTPUT_DIR)/*.blg $(OUTPUT_DIR)/*.bcf
	rm -f $(OUTPUT_DIR)/*.run.xml $(OUTPUT_DIR)/*.fls $(OUTPUT_DIR)/*.fdb_latexmk
	rm -f $(OUTPUT_DIR)/*.synctex.gz
	rm -f $(PAPERS_DIR)/*.aux $(PAPERS_DIR)/*.log $(PAPERS_DIR)/*.out
	rm -f $(PAPERS_DIR)/*.toc $(PAPERS_DIR)/*.lof $(PAPERS_DIR)/*.lot
	@echo "Done!"

# Clean everything including PDFs
.PHONY: distclean
distclean: clean
	@echo "Removing all generated files..."
	rm -rf $(OUTPUT_DIR)
	@echo "Done!"

# Help target
.PHONY: help
help:
	@echo "LaTeX Build System"
	@echo "=================="
	@echo ""
	@echo "Targets:"
	@echo "  all          - Build all papers (default)"
	@echo "  esl          - Build ESL Paper"
	@echo "  esl-full     - Build ESL Paper with bibliography"
	@echo "  watch        - Watch for changes and auto-rebuild"
	@echo "  install-deps - Install LaTeX dependencies"
	@echo "  check        - Check LaTeX installation"
	@echo "  clean        - Remove build artifacts"
	@echo "  distclean    - Remove all generated files"
	@echo "  help         - Show this help message"
