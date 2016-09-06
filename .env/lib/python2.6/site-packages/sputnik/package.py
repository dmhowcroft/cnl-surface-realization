import os
import logging

from . import util
from . import default
from .package_stub import PackageStub


class NotIncludedException(Exception): pass


class Package(PackageStub):  # installed package
    def __init__(self, path):
        meta = util.json_load(os.path.join(path, default.META_FILENAME))
        super(Package, self).__init__(defaults=meta['package'])

        self.logger = logging.getLogger(__name__)
        self.meta = meta
        self.path = path

    @property
    def manifest(self):
        return self.meta['manifest']

    def has_file(self, *path_parts):
        return any(m for m in self.manifest if tuple(m['path']) == path_parts)

    def file_path(self, *path_parts):
        path = util.get_path(*path_parts)

        if not self.has_file(*path_parts):
            raise NotIncludedException('package does not include file: %s' % path)

        return os.path.join(self.path, path)

    def dir_path(self, *path_parts):
        # TODO check whether path is part of package
        path = util.get_path(*path_parts)
        return os.path.join(self.path, path)
