import os
import io

from . import util
from . import default
from .package_stub import PackageStub
from .archive_reader import ArchiveReader


class Archive(PackageStub):
    def __init__(self, path):
        self.archive = ArchiveReader(path)
        defaults = self.archive.get_member('package')
        super(Archive, self).__init__(defaults)

        self.path = path

    @property
    def manifest(self):
        return self.archive.get_member('manifest')

    def fileobjs(self):
        return {
            os.path.join(self.ident, default.META_FILENAME):
                io.BytesIO(util.json_dump(self.archive.meta)),
            os.path.join(self.ident, default.ARCHIVE_FILENAME):
                self.archive.archive
        }
