SHELL := bash

# Environment variables.
export PYTHONPATH := $(CURDIR):$(PYTHONPATH)
export MAX_LINE_LENGTH := 79

# Default game settings for `run`.
DEFAULT_WIDTH := 10
DEFAULT_HEIGHT := 10
DEFAULT_DELAY := 0.5

# Verbosity settings.
V_FLAGS := $(if $V,$(foreach n,$(shell seq $(V)),-v),)

# Build everything needed to install.
.PHONY: build
build:
	python setup.py build

# Install everything from build directory.
.PHONY: install
install:
	python setup.py install

# Install in development mode.
.PHONY: develop
develop:
	python setup.py develop

# Install deps.
.PHONY: deps
deps:
	pip install $(V_FLAGS) -r requirements.dev.txt

# Format code.
.PHONY: fmt
fmt:
	pyfmt

# Run tests.
.PHONY: test
test:
	py.test $(if $V,--verbosity=$V)

# Format + test.
.PHONY: check
check: fmt test
	python setup.py check

# Run app.
W ?= $(if $(WIDTH),$(WIDTH),$(DEFAULT_WIDTH))
H ?= $(if $(HEIGHT),$(HEIGHT),$(DEFAULT_HEIGHT))
DELAY := --delay $(if $(DELAY),$(DELAY),$(DEFAULT_DELAY))
SEP := $(if $(SEPARATOR), --separator $(SEPARATOR))
PAD := $(if $(PADDING), --padding $(PADDING))
OUT := $(if $(OUTFILE), --outfile $(OUTFILE))
.PHONY: run
run:
	python conway $(DELAY)$(SEP)$(PAD)$(OUT) -- $(W) $(H)
