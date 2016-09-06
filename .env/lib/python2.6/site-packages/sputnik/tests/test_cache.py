import pytest

from ..cache import Cache
from ..package_stub import PackageStub
from ..package_list import (CompatiblePackageNotFoundException,
                            PackageNotFoundException)


def test_list(tmp_path):
    cache = Cache('test', '1.0.0', tmp_path)

    for i in range(1, 5):
        package = PackageStub({'name': 'abc', 'version': '%d.0.0' % i})
        cache.update({
            'archive': ['archive.gz', None],
            'package': package.to_dict()
        }, None)

    assert len(cache.find('xyz')) == 0

    assert len(cache.find()) == 4
    assert len(cache.find('')) == 4

    assert len(cache.find('abc')) == 4
    assert len(cache.find('abc ==1.0.0')) == 1
    assert len(cache.find('abc ==0.1.0')) == 0
    assert len(cache.find('abc>=1.9.0')) == 3


def test_update(tmp_path):
    cache = Cache('test', '1.0.0', tmp_path)
    package = PackageStub({'name': 'abc', 'version': '1.0.0'})

    meta = {
        'archive': ['archive.gz', None],
        'package': package.to_dict()
    }

    assert len(cache.find()) == 0

    cache.update(meta, None)

    assert len(cache.find()) == 1
    assert cache.find()[0].ident == package.ident

    with pytest.raises(CompatiblePackageNotFoundException):
        assert cache.get('abc >=1.0.1')

    assert cache.get('abc').ident == package.ident
    assert cache.get('abc ==1.0.0').ident == package.ident
    assert cache.get('abc >0.0.1').ident == package.ident

    with pytest.raises(PackageNotFoundException):
        assert cache.get('xyz')


def test_remove(tmp_path):
    cache = Cache('test', '1.0.0', tmp_path)
    package = PackageStub({'name': 'abc', 'version': '1.0.0'})

    meta = {
        'archive': ['archive.gz', None],
        'package': package.to_dict()
    }

    assert len(cache.find()) == 0

    cache.update(meta, None)

    assert len(cache.find()) == 1
    assert cache.find()[0].ident == package.ident

    package = cache.get('abc')
    cache.remove(package)

    assert len(cache.find()) == 0

    with pytest.raises(PackageNotFoundException):
        assert cache.get('abc')


def test_update_compatible(tmp_path):
    cache = Cache('test', '1.0.0', tmp_path)
    package = PackageStub({
        'name': 'abc',
        'version': '1.0.0',
        'compatibility': {
            'test': None
        }
    })

    meta = {
        'archive': ['archive.gz', None],
        'package': package.to_dict()
    }

    assert len(cache.find()) == 0

    cache.update(meta, None)

    assert len(cache.find()) == 1

    with pytest.raises(CompatiblePackageNotFoundException):
        assert cache.get('abc >=1.0.1')

    assert cache.get('abc').ident == package.ident
    assert cache.get('abc ==1.0.0').ident == package.ident
    assert cache.get('abc >0.0.1').ident == package.ident

    with pytest.raises(PackageNotFoundException):
        assert cache.get('xyz')


def test_update_incompatible(tmp_path):
    cache = Cache('test', '1.0.0', tmp_path)
    package = PackageStub({
        'name': 'abc',
        'version': '1.0.0',
        'compatibility': {
            'test': None
        }
    })

    meta = {
        'archive': ['archive.gz', None],
        'package': package.to_dict()
    }

    assert len(cache.find()) == 0

    cache.update(meta, None)

    assert len(cache.find()) == 1

    with pytest.raises(PackageNotFoundException):
        assert cache.get('xyz')


def test_update_multiple_compatible(tmp_path):
    cache = Cache('test', '5.0.0', tmp_path)

    for i in range(1, 11):
        package = PackageStub({
            'name': 'abc',
            'version': '%d.0.0' % i,  # from 1.0.0 to 10.0.0
            'compatibility': {
                'test': None
            }
        })

        meta = {
            'archive': ['archive.gz', None],
            'package': package.to_dict()
        }

        cache.update(meta, None)

    assert len(cache.find()) == 10
    assert cache.get('abc').version == '10.0.0'

    with pytest.raises(PackageNotFoundException):
        assert cache.get('xyz')


def test_update_multiple_incompatible(tmp_path):
    cache = Cache('test', '0.0.0', tmp_path)

    for i in range(1, 11):
        package = PackageStub({
            'name': 'abc',
            'version': '%d.0.0' % i,  # from 1.0.0 to 10.0.0
            'compatibility': {
                'test': None
            }
        })

        meta = {
            'archive': ['archive.gz', None],
            'package': package.to_dict()
        }

        cache.update(meta, None)

    assert len(cache.find()) == 10

    with pytest.raises(PackageNotFoundException):
        assert cache.get('xyz')
