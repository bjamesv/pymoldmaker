"""
Simple module defining unittest2 testcases for project doctests
"""
import doctest

from . import kerf
import ImportMesh

def load_tests(loader, tests, ignore):
    """
    add doctests for this package
    """
    tests.addTests(doctest.DocTestSuite(ImportMesh))
    tests.addTests(doctest.DocTestSuite("ImportMesh.Part"))
    tests.addTests(doctest.DocTestSuite("ImportMesh.PartSection"))
    tests.addTests(doctest.DocTestSuite("ImportMesh.VectorMesh"))
    tests.addTests(doctest.DocTestSuite("ImportMesh.Mesh"))
    tests.addTests(doctest.DocTestSuite(kerf))
    return tests
