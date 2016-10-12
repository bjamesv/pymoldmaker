#!/bin/sh
# Set up required python packages, per:
# pycollada.readthedocs.org/en/latest/install.html
python3 -m virtualenv pymoldmaker-env
source pymoldmaker-env/bin/activate && pip install -r requirements.txt
