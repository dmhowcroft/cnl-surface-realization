import os

from . import default
from .pool import Pool
from .util import expand_path, json_print, default_data_path
from .package import Package
from .recipe import Recipe
from .archive import Archive
from .cache import Cache
from .index import Index


# TODO support asterisks in package_strings


def install(app_name,
            app_version,
            package_name,
            data_path=None,
            repository_url=None):

    if data_path is None:
        data_path = default_data_path(app_name)
    if repository_url is None:
        repository_url = default.repository_url

    package_name = expand_path(package_name)
    data_path = expand_path(data_path)

    pool = Pool(app_name, app_version, data_path)

    if os.path.isfile(package_name):
        archive = Archive(package_name)

    else:
        index = Index(app_name, app_version, data_path, repository_url)
        index.update()

        packages = pool.find(package_name)
        if packages:
            return packages[0]

        cache = Cache(app_name, app_version, data_path)
        archive = cache.fetch(package_name)

    path = pool.install(archive)
    return Package(path=path)


def build(package_path=None,
          archive_path=None):

    if package_path is None:
        package_path = default.build_package_path

    recipe = Recipe(expand_path(package_path))
    return recipe.build(expand_path(archive_path or package_path))


def remove(app_name,
           app_version,
           package_string,
           data_path=None):

    if data_path is None:
        data_path = default_data_path(app_name)

    pool = Pool(app_name, app_version, expand_path(data_path))
    packages = pool.find(package_string)
    for pkg in packages:
        pool.remove(pkg)


def search(app_name,
           app_version,
           search_string=None,
           data_path=None,
           repository_url=None):

    if search_string is None:
        search_string = default.search_string
    if data_path is None:
        data_path = default_data_path(app_name)
    if repository_url is None:
        repository_url = default.repository_url

    # TODO make it work without data path?
    index = Index(app_name, app_version, data_path, repository_url)
    index.update()

    cache = Cache(app_name, app_version, data_path)
    packages = cache.find(search_string)
    json_print([p.ident for p in packages])
    return packages


def find(app_name,
         app_version,
         package_string=None,
         meta=None,
         cache=None,
         data_path=None):

    if package_string is None:
        package_string = default.find_package_string
    if meta is None:
        meta = default.find_meta
    if cache is None:
        cache = default.find_cache
    if data_path is None:
        data_path = default_data_path(app_name)

    cls = cache and Cache or Pool
    obj = cls(app_name, app_version, expand_path(data_path))
    packages = obj.find(package_string)
    keys = not meta and ('name', 'version') or ()
    json_print([p.to_dict(keys) for p in packages])
    return packages


def upload(app_name,
           app_version,
           package_path,
           data_path=None,
           repository_url=None):

    if data_path is None:
        data_path = default_data_path(app_name)
    if repository_url is None:
        repository_url = default.repository_url

    # TODO make it work without data path?
    index = Index(app_name, app_version, data_path, repository_url)
    return index.upload(expand_path(package_path))


def update(app_name,
           app_version,
           data_path=None,
           repository_url=None):

    if data_path is None:
        data_path = default_data_path(app_name)
    if repository_url is None:
        repository_url = default.repository_url

    index = Index(app_name, app_version, expand_path(data_path), repository_url)
    index.update()


def package(app_name,
            app_version,
            package_string,
            data_path=None):

    if data_path is None:
        data_path = default_data_path(app_name)

    pool = Pool(app_name, app_version, expand_path(data_path))
    return pool.get(package_string)


def files(app_name,
          app_version,
          package_string,
          data_path=None):

    if data_path is None:
        data_path = default_data_path(app_name)

    if os.path.isfile(package_string):
        obj = Archive(package_string)
    else:
        pool = Pool(app_name, app_version, expand_path(data_path))
        obj = pool.get(package_string)

    res = dict([(os.path.sep.join(f['path']), {'checksum': f['checksum'], 'size': f['size']})
                for f in obj.manifest])
    json_print({obj.ident: res})
    return res


def purge(app_name,
          app_version,
          cache=None,
          pool=None,
          data_path=None):

    if cache is None:
        cache = default.purge_cache
    if pool is None:
        pool = default.purge_pool
    if data_path is None:
        data_path = default_data_path(app_name)

    data_path = expand_path(data_path)

    if cache or not cache and not pool:
        Cache(app_name, app_version, data_path).purge()

    if pool or not cache and not pool:
        Pool(app_name, app_version, data_path).purge()
