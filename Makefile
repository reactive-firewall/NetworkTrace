#!/usr/bin/env make -f


ifeq "$(ECHO)" ""
	ECHO=echo
endif

ifeq "$(CP)" ""
	CP=cp -v
endif

ifeq "$(CHMOD)" ""
	CHMOD=chmod
endif

ifeq "$(CHOWN)" ""
	CHOWN=chown
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
	$(QUIET)$(CP) code/record_pcap.py /usr/local/bin/record_pcap.py
	$(QUIET)$(CP) code/analyze_pcap.py /usr/local/bin/analyze_pcap.py
	$(QUIET)$(CHMOD) 755 /usr/local/bin/record_pcap.py
	$(QUIET)$(CHMOD) 755 /usr/local/bin/analyze_pcap.py
	$(QUIET)$(CHOWN) 0:0 /usr/local/bin/record_pcap.py
	$(QUIET)$(CHOWN) 0:0 /usr/local/bin/analyze_pcap.py
	$(QUIET)$(ECHO) "$@: Done."

test:
	$(QUIET)python -m unittest tests.test_basic

clean:
	$(QUIET)rm -vf tests/*.pyc 2 >> /dev/null
	$(QUIET)rm -vf code/*.pyc 2 >> /dev/null

%:
	$(QUIET)$(ECHO) "No Rule Found For $@" ; $(WAIT) ;
