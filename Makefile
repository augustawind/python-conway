SHELL := bash

# Environment variables.
export PYTHONPATH := $(CURDIR):$(PYTHONPATH)
export MAX_LINE_LENGTH := 79

# Default game settings for `run`.
DEFAULT_WIDTH := 10
DEFAULT_HEIGHT := 10
DEFAULT_DELAY := 0.5

# Verbosity settings.
V ?= 1
Q := $(if $V,,@)
V_FLAGS := $(if $V,$(foreach n,$(shell seq $(V)),-v),)

.PHONY: deps fmt test check run

deps:
	$Q pip install $(V_FLAGS) -r requirements.dev.txt

fmt:
	$Q pyfmt

test:
	$Q py.test $(if $V,--verbosity=$V)

check: fmt test

W ?= $(if $(WIDTH),$(WIDTH),$(DEFAULT_WIDTH))
H ?= $(if $(HEIGHT),$(HEIGHT),$(DEFAULT_HEIGHT))
DELAY := --delay $(if $(DELAY),$(DELAY),$(DEFAULT_DELAY))
SEP := $(if $(SEPARATOR), --separator $(SEPARATOR))
PAD := $(if $(PADDING), --padding $(PADDING))
OUT := $(if $(OUTFILE), --outfile $(OUTFILE))

run:
	$Q python conway $(DELAY)$(SEP)$(PAD)$(OUT) -- $(W) $(H)
