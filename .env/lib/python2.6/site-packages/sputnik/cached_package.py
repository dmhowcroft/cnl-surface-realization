import os
import logging

from . import util
from . import default
from .package_stub import PackageStub


class CachedPackage(PackageStub):
    def __init__(self, path):
        meta = util.json_load(os.path.join(path, default.META_FILENAME))
        super(CachedPackage, self).__init__(defaults=meta['package'])

        self.logger = logging.getLogger(__name__)
        self.meta = meta
        self.path = path

    @property
    def manifest(self):
        return self.meta['manifest']
