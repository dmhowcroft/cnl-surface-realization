import os
import json

import pytest

from ..recipe import Recipe
from ..package import Package, NotIncludedException
from ..archive import Archive
from ..pool import Pool
from ..dir_package import DirPackage


def test_build_and_check_archive(tmp_path, sample_package_path):
    recipe = Recipe(sample_package_path)
    archive1 = recipe.build(tmp_path)

    assert os.path.isfile(archive1.path)

    archive2 = Archive(archive1.path)

    for key in Archive.keys:
        assert getattr(archive1, key) == getattr(archive2, key)


def test_package_file_load(tmp_path, tmp_path2, sample_package_path):
    recipe = Recipe(sample_package_path)
    archive = Archive(recipe.build(tmp_path).path)
    pool = Pool('test', '1.0.0', tmp_path2)
    path = pool.install(archive)
    package = Package(path=path)

    assert package.path == path

    assert package.has_file('data', 'xyz.json')
    assert not package.has_file('data', 'foo')

    with package.open(['data', 'xyz.json']) as f:
        assert json.load(f) == {'test': True}

    with package.open(['data', 'xyz.json'], mode='rb', encoding=None) as f:
        data = f.read()
        assert data == json.dumps({'test': True}).encode('ascii')
        assert data == b'{"test": true}'

    with package.open(['data', 'foo'], default=0) as f:
        assert f == 0

    with package.open(['data', 'foo'], default=None) as f:
        assert f is None

    with pytest.raises(Exception):
        with package.open(['data', 'foo'], default=Exception) as f:
           pass


def test_package_file_path(tmp_path, tmp_path2, sample_package_path):
    recipe = Recipe(sample_package_path)
    archive = Archive(recipe.build(tmp_path).path)
    pool = Pool('test', '1.0.0', tmp_path2)
    path = pool.install(archive)
    package = Package(path=path)

    assert package.path == path

    assert package.has_file('data', 'xyz.model')
    assert package.file_path('data', 'xyz.model') == os.path.join(package.path, 'data', 'xyz.model')
    assert package.dir_path('data') == os.path.join(package.path, 'data')

    assert not package.has_file('data')
    assert not package.has_file('data', 'model')
    with pytest.raises(NotIncludedException):
        assert package.file_path('data', 'model')


def test_file_path_same_build_directory(tmp_path, sample_package_path):
    recipe = Recipe(sample_package_path)
    archive = Archive(recipe.build(sample_package_path).path)
    pool = Pool('test', '1.0.0', tmp_path)
    package = Package(path=pool.install(archive))

    assert package.has_file('data', 'xyz.model')
    assert package.file_path('data', 'xyz.model') == os.path.join(package.path, 'data', 'xyz.model')
    assert package.dir_path('data') == os.path.join(package.path, 'data')

    assert not package.has_file('data')
    assert not package.has_file('data', 'model')
    with pytest.raises(NotIncludedException):
        assert package.file_path('data', 'model')


@pytest.mark.xfail
def test_new_archive_files(tmp_path, sample_package_path):
    recipe = Recipe(sample_package_path)
    archive = recipe.build(tmp_path)

    assert archive.manifest
    assert set([m['path'] for m in archive.manifest]) == \
           set([('data', 'xyz.model'), ('data/xyz.json')])


def test_archive_files(tmp_path, sample_package_path):
    recipe = Recipe(sample_package_path)
    new_archive = recipe.build(tmp_path)
    archive = Archive(new_archive.path)

    assert archive.manifest
    assert set([tuple(m['path']) for m in archive.manifest]) == \
           set([('data', 'xyz.model'), ('data', 'xyz.json')])


def test_dir_package(sample_package_path):
    package = DirPackage(sample_package_path)

    assert package.path == sample_package_path

    assert package.has_file('data', 'xyz.json')
    assert not package.has_file('data', 'foo')

    assert package.dir_path('data') == os.path.join(sample_package_path, 'data')
    assert package.file_path('data', 'xyz.model') == os.path.join(sample_package_path, 'data', 'xyz.model')

    assert package.dir_path('data') == os.path.join(sample_package_path, 'data')

    with package.open(['data', 'xyz.json']) as f:
        assert json.load(f) == {'test': True}

    with package.open(['data', 'xyz.json'], mode='rb', encoding=None) as f:
        assert f.read() == json.dumps({'test': True}).encode('ascii') == b'{"test": true}'
