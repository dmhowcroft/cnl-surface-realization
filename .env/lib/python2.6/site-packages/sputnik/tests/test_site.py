import os
import subprocess
import shutil

import pytest

from .. import site


def pip_uninstall(package_name):
    subprocess.call(['pip', 'uninstall', '-yq', package_name])


def pip_install(package_name):
    subprocess.call(['pip', 'install', '-q', package_name])


@pytest.fixture
def package_name():
    return 'text_unidecode'


@pytest.fixture
def record_path():
    return site.get_record_path('setuptools')


def test_pip(package_name):
    pip_install(package_name)
    try:
        path = site.get_mod_path(package_name)
        assert os.path.exists(path)
    finally:
        pip_uninstall(package_name)
        assert not os.path.exists(path)


def test_get_record_path():
    assert site.get_record_path('setuptools')


def test_record_has_path(package_name, record_path):
    assert site.record_has_path(record_path, 'setuptools/__init__.py')


def test_record_has_path(record_path):
    assert site.record_has_path(record_path, 'setuptools/__init__.py')


def test_record_add_path(package_name):
    pip_install(package_name)
    try:
        path = site.get_mod_path(package_name)
        assert os.path.exists(path)

        record_path = site.get_record_path(package_name)
        assert record_path

        assert site.record_has_path(record_path, '%s/__init__.py' % package_name)
        assert not site.record_has_path(record_path, '%s/data' % package_name)
        site.record_add_path(record_path, '%s/data' % package_name)
        assert site.record_has_path(record_path, '%s/data' % package_name)
    finally:
        pip_uninstall(package_name)
        assert not os.path.exists(path)


def test_add_path(package_name):
    pip_install(package_name)
    try:
        path = site.get_mod_path(package_name)
        assert os.path.exists(path)

        record_path = site.get_record_path(package_name)
        assert record_path

        data_path = os.path.join(path, 'data')
        assert not os.path.exists(data_path)
        os.mkdir(data_path)

        assert not site.record_has_path(record_path, '%s/data' % package_name)
        site.add_path(package_name, 'data')
        assert site.record_has_path(record_path, '%s/data' % package_name)
    finally:
        pip_uninstall(package_name)
        assert not os.path.exists(path)


@pytest.mark.xfail
def test_add_outside_path(package_name):
    pip_install(package_name)
    try:
        path = site.get_mod_path(package_name)
        assert os.path.exists(path)

        record_path = site.get_record_path(package_name)
        assert record_path

        assert not site.record_has_path(record_path, 'data')
        site.add_path(record_path, '../data')
        assert not site.record_has_path(record_path, '../data')

        assert not os.path.exists(path)
    finally:
        pip_uninstall(package_name)
        assert not os.path.exists(path)
