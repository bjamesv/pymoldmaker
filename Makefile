# -*- indent-tabs-mode:t; -*-

.PHONY: test debug

test	: *
	python3 -m unittest discover

debug	:
	python3 -m pdb vector.py

