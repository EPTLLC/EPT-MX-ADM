"""
Minimal test for CI verification
"""

def test_basic():
    """Most basic test possible"""
    assert True


def test_math():
    """Basic math test"""
    assert 1 + 1 == 2


def test_string():
    """Basic string test"""
    assert "hello" == "hello"


def test_list():
    """Basic list test"""
    assert len([1, 2, 3]) == 3


def test_dict():
    """Basic dict test"""
    data = {"key": "value"}
    assert data["key"] == "value" 