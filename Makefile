#!/usr/bin/env make -f

ifeq "$(ECHO)" ""
	ECHO=echo
endif

ifeq "$(LOG)" ""
	LOG=no
endif

ifeq "$(LOG)" "no"
	QUIET=@
endif

build:
	$(QUIET)$(ECHO) "No need to build. Try make -f Makefile install"

init:
	$(QUIET)$(ECHO) "$@: Done."

install:
	$(QUIET)$(ECHO) "$@: Done."

test:
	nosetests tests

%:
	$(QUIET)$(ECHO) "No Rule Found For $@" ; $(WAIT) ;