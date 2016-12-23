"""
Simple module defining unittest2 testcases for project doctests
"""
import doctest
import vector, image

def load_tests(loader, tests, ignore):
    """
    add doctests for this package
    """
    tests.addTests(doctest.DocTestSuite(vector))
    tests.addTests(doctest.DocTestSuite(image))
    return tests
