#!/bin/sh
# Set up required python packages, per:
# pycollada.readthedocs.org/en/latest/install.html
sudo apt-get install python3-lxml python3-numpy python3-dateutil python3-pip python-imaging
sudo python3 -m easy_install pycollada
