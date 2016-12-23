"""
Simple module defining unittest2 testcases for project doctests
"""
import doctest

from . import test_cube_flipped

def load_tests(loader, tests, ignore):
    """
    add doctests for this package
    """
    tests.addTests(doctest.DocTestSuite(test_cube_flipped))
    return tests
