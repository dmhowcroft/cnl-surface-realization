import gzip
import io
import os
import tarfile
import time
import tempfile
import hashlib
import shutil
import logging

from . import util
from . import default


class EmptyArchiveException(Exception): pass
class InvalidPathException(Exception): pass


class ArchiveWriter(object):
    def __init__(self, path, base_path=None):
        self.logger = logging.getLogger(__name__)

        self.base_path = base_path
        self.path = path
        self.tmp_path = tempfile.mkdtemp()
        self.tmp_archive_path = os.path.join(self.tmp_path, default.ARCHIVE_FILENAME)
        self.archive = io.open(self.tmp_archive_path, 'wb')
        self.meta = {'manifest': []}

    def cleanup(self):
        shutil.rmtree(self.tmp_path)
        assert not os.path.exists(self.tmp_path)

    def close(self):
        self.archive.close()

        if not self.meta['manifest']:
            self.cleanup()
            raise EmptyArchiveException(self.path)

        mtime = time.time()

        tar = tarfile.open(self.path, 'w')
        with io.open(self.tmp_archive_path, 'rb') as f:
            checksum = hashlib.md5(f.read()).hexdigest()
            f.seek(os.SEEK_SET, 0)

            info = tarfile.TarInfo(default.ARCHIVE_FILENAME)
            info.size = os.stat(self.tmp_archive_path).st_size
            info.mtime = os.stat(self.tmp_archive_path).st_mtime
            info.type = tarfile.REGTYPE
            info.mode = 0o644
            info.uid = info.gid = 1000
            tar.addfile(info, f)
            self.meta['archive'] = (default.ARCHIVE_FILENAME, checksum)

        data = util.json_dump(self.meta)
        with io.BytesIO(data) as f:
            info = tarfile.TarInfo(default.META_FILENAME)
            info.size = len(data)
            info.mtime = mtime
            info.type = tarfile.REGTYPE
            info.mode = 0o644
            info.uid = info.gid = 1000
            tar.addfile(info, f)
        tar.close()

        self.cleanup()

    def add_json(self, name, obj):
        self.logger.info("adding %s", name)
        self.meta[name] = obj

    def add(self, path, cb=None):
        self.logger.info("adding %s", path)
        if self.base_path is None and os.path.isabs(path):
            raise InvalidPathException('cannot handle absolute paths without base_path: %s' % path)

        checksum = hashlib.md5()

        gz = gzip.GzipFile(fileobj=self.archive,
                           compresslevel=default.COMPRESSLEVEL)
        with io.open(path, 'rb') as f:
            bytes_read = 0

            while True:
                chunk = f.read(default.CHUNK_SIZE)
                if not chunk:
                    break

                bytes_read += len(chunk)

                gz.write(chunk)
                checksum.update(chunk)

                # callback for progress tracking
                if cb:
                    cb(bytes_read)

        gz.close()

        meta_path = os.path.relpath(path, self.base_path or '').split(os.path.sep)

        self.meta['manifest'].append({
            'path': meta_path,
            'noffset': self.archive.tell(),
            'size': os.stat(path).st_size,
            'checksum': (checksum.name, checksum.hexdigest()),
        })

    def add_path(self, path, cb=None):
        for root, _, filenames in os.walk(path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                self.add(file_path, cb=cb)
