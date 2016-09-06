import os

from .package_stub import PackageStub


class DirPackage(PackageStub):

    def __init__(self, path):
        self.path = path

    def has_file(self, *path_parts):
        return os.path.isfile(os.path.join(self.path, *path_parts))

    def file_path(self, *path_parts):
        return os.path.join(self.path, *path_parts)

    def dir_path(self, *path_parts):
        return os.path.join(self.path, *path_parts)
