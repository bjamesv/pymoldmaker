# -*- indent-tabs-mode:t; -*-

include Makefile.properties.mk

.PHONY: test debug

test	: *
	. ${env_cmd} && python3 -m unittest discover

debug	:
	. ${env_cmd} && python3 -m pdb vector.py

