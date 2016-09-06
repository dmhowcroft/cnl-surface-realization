import os

import pytest

from .. import install, build, remove, search, find, upload, update, files, purge


repository_url = os.environ.get('REPOSITORY_URL', 'https://index-staging.spacy.io')


@pytest.mark.remote
def test_upload_package(sample_package_path, tmp_path):
    archive = build(sample_package_path)
    assert os.path.isfile(archive.path)

    res = upload(None, None, archive.path, data_path=tmp_path, repository_url=repository_url)
    assert res


@pytest.mark.remote
def test_upload_package2(sample_package_path2, tmp_path):
    archive = build(sample_package_path2)
    assert os.path.isfile(archive.path)

    res = upload(None, None, archive.path, data_path=tmp_path, repository_url=repository_url)
    assert res


@pytest.mark.remote
def test_install_package(tmp_path):
    packages = find(None, None, data_path=tmp_path)
    assert len(packages) == 0

    package = install(None, None, 'test', data_path=tmp_path, repository_url=repository_url)
    assert os.path.isdir(package.path)

    packages = find(None, None, data_path=tmp_path)
    assert len(packages) == 1
    assert packages[0].ident == package.ident


@pytest.mark.remote
def test_upgrade_package(tmp_path):
    packages = find(None, None, data_path=tmp_path)
    assert len(packages) == 0

    package1 = install(None, None, 'test ==1.0.0', data_path=tmp_path, repository_url=repository_url)
    assert os.path.isdir(package1.path)

    packages = find(None, None, data_path=tmp_path)
    assert len(packages) == 1
    assert packages[0].ident == package1.ident

    package2 = install(None, None, 'test ==2.0.0', data_path=tmp_path, repository_url=repository_url)
    assert os.path.isdir(package2.path)

    packages = find(None, None, data_path=tmp_path)
    assert len(packages) == 1
    assert packages[0].ident == package2.ident


@pytest.mark.remote
def test_search_packages(tmp_path):
    assert search(None, None, data_path=tmp_path, repository_url=repository_url)
