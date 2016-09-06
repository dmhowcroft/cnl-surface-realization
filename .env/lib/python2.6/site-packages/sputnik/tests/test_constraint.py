import pytest

from ..util import constraint_match
from ..package_stub import PackageStub


def test_string_match():
    x = PackageStub(dict(name='test', version='1.0.0'))
    y = PackageStub(dict(name='test', version='1.0.0'))
    assert x.name == y.name
    assert x.version == y.version
    assert x == y


def test_no_string_match():
    x = PackageStub(dict(name='test', version='1.0.0'))
    y = PackageStub(dict(name='abc', version='1.0.0'))
    assert x.name != y.name
    assert x.version == y.version
    with pytest.raises(Exception):
        x != y


def test_version_match():
    assert constraint_match('>=1.0.0', '1.0.0')
    assert constraint_match('==1.0.0', '1.0.0')
    assert constraint_match('<=1.0.0', '1.0.0')
    assert constraint_match('>1.0.0', '1.1.0')
    assert constraint_match('<1.0.0', '0.1.0')

    assert constraint_match(' >=1.0.0', '1.0.0')
    assert constraint_match(' ==1.0.0', '1.0.0')
    assert constraint_match(' <=1.0.0', '1.0.0')
    assert constraint_match(' >1.0.0', '1.1.0')
    assert constraint_match(' <1.0.0', '0.1.0')


def test_no_version_match():
    assert not constraint_match('>=1.0.0 , <=1.0.0', '0.1.0')
    assert not constraint_match('==1.0.0, <=1.0.0', '0.1.0')
    assert not constraint_match('<=1.0.0 ,<=1.0.0', '1.1.0')
    assert not constraint_match('>1.0.0 , <=1.0.0,,', '0.1.0')
    assert not constraint_match('<1.0.0 ,, <=1.0.0', '1.1.0')

    assert not constraint_match(' >=1.0.0', '0.1.0')
    assert not constraint_match(' ==1.0.0', '0.1.0')
    assert not constraint_match(' <=1.0.0', '1.1.0')
    assert not constraint_match(' >1.0.0', '0.1.0')
    assert not constraint_match(' <1.0.0', '1.1.0')
