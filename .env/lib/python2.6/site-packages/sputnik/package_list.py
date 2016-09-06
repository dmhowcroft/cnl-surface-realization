import os
import logging
import shutil

from . import default
from . import util
from .package_stub import PackageStub


class PackageNotFoundException(Exception): pass
class CompatiblePackageNotFoundException(Exception): pass
class InvalidDataPathException(Exception): pass


class PackageList(object):

    package_class = PackageStub

    def __init__(self, app_name, app_version, path, **kwargs):
        super(PackageList, self).__init__()

        self.logger = logging.getLogger(__name__)

        self.app_name = app_name
        self.app_version = app_version

        self.path = path
        self.data_path = kwargs.get('data_path') or path

        if not self.data_path:
            raise InvalidDataPathException(self.data_path)

        self.load()

    def packages(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        for path in os.listdir(self.path):
            if path.endswith('.tmp'):
                continue

            meta_path = os.path.join(self.path, path, default.META_FILENAME)
            if not os.path.isfile(meta_path):
                continue

            yield self.__class__.package_class(path=os.path.join(self.path, path))

    def load(self):
        self._packages = {}
        for package in self.packages():
            self._packages[package.ident] = package

    def get(self, package_string):
        candidates = self.find(util.split_package_string(package_string)[0])
        if not candidates:
            raise PackageNotFoundException(package_string)

        candidates = sorted(self.find(package_string))
        if not candidates:
            raise CompatiblePackageNotFoundException(package_string)
        return candidates[-1]

    def find(self, package_string=None):
        res = []
        for package in self._packages.values():
            name, constraint = util.split_package_string(package_string)
            if not name or name == package.name and util.constraint_match(constraint, package.version):
                res.append(package)
        return res

    def purge(self):
        self.logger.info('purging %s', self.__class__.__name__)
        for package in self.find():
            self.remove(package)

    def remove(self, package):
        if not os.path.isdir(package.path):
            raise Exception('Package not correctly installed: %s' % package.ident)

        # cleanup remove
        if os.path.exists(package.path):
            self.logger.info('pending remove %s', package.ident)
            tmp = package.path + '.tmp'
            shutil.move(package.path, tmp)
            self.logger.info('remove %s', package.ident)
            shutil.rmtree(tmp)

        self.load()
