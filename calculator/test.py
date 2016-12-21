"""
Simple module defining unittest2 testcases for project doctests
"""
import doctest

from . import (
     Mesh
    ,Part
    ,PartSection
    ,calculator
    ,kerf
)

def load_tests(loader, tests, ignore):
    """
    add doctests for this package
    """
    tests.addTests(doctest.DocTestSuite(Part))
    tests.addTests(doctest.DocTestSuite(PartSection))
    tests.addTests(doctest.DocTestSuite(calculator))
    tests.addTests(doctest.DocTestSuite(Mesh))
    tests.addTests(doctest.DocTestSuite(kerf))
    return tests
