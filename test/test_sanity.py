"""Sanity tests for pytest."""
from pytest import mark


@mark.xfail
def test_fail():
    raise AssertionError()


def test_pass():
    assert True
