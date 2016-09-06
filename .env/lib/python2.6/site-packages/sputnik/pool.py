import os
import shutil
import logging

from . import util
from .package import Package
from .package_list import PackageList


class NotEnoughSpaceException(Exception): pass
class PackageAlreadyInstalledException(Exception): pass


class Pool(PackageList):

    package_class = Package

    def __init__(self, app_name, app_version, path, **kwargs):
        super(Pool, self).__init__(app_name, app_version, path, **kwargs)
        self.logger = logging.getLogger(__name__)
        self.cleanup()

    def cleanup(self):
        for filename in os.listdir(self.path):
            if filename.endswith('.tmp'):
                self.logger.info('remove %s', filename)
                shutil.rmtree(os.path.join(self.path, filename))

    def install(self, archive):
        for pkg in self.find(archive.name):
            if archive.ident == pkg.ident:
                raise PackageAlreadyInstalledException(pkg.ident)

        if not util.is_enough_space(self.path, archive.archive.size()):
            raise NotEnoughSpaceException('requires %0.2f MB' %
                                          (archive.archive.size() / 1024 / 1024))

        # remove installed versions of same package
        for pkg in self.find(archive.name):
            self.remove(pkg)

        archive_name = util.archive_filename(archive.name, archive.version)
        path = os.path.join(self.path, archive_name)

        self.logger.info('install %s', os.path.basename(path))
        archive.archive.extract_all(path + '.tmp')
        os.rename(path + '.tmp', path)

        return path
