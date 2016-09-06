import gzip
import io
import os
import hashlib
import json
import tarfile
import codecs
import shutil

from . import default
from . import util


class ArchiveReader(object):
    def __init__(self, path):
        self.path = path
        self.archive = None

        if os.path.isdir(path):
            self.tar = None
            self.meta = util.json_load(os.path.join(path, default.META_FILENAME))
            self.archive = io.open(os.path.join(path, self.filename()), 'rb')

        else:  # expect tar
            self.tar = tarfile.open(self.path, 'r')
            self.meta = self.get_meta()
            self.archive = self.tar.extractfile(self.filename())

    def filename(self):
        return os.path.basename(self.meta['archive'][0])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if isinstance(exc_value, Exception):
            return False
        self.close()

    def close(self):
        self.archive.close()
        self.tar.close()

    def extract(self, member, extract_path, cb=None):
        noffset = 0
        for entry in self.meta['manifest']:
            if entry['path'] == member:
                path = os.path.sep.join(entry['path'])
                size = entry['size']

                self.archive.seek(noffset)

                checksum = getattr(hashlib, entry['checksum'][0])()

                gz = gzip.GzipFile(fileobj=self.archive)

                filename = os.path.join(extract_path, path)
                util.makedirs(filename)
                with io.open(filename, 'wb') as f:

                    bytes_read = 0
                    while True:
                        chunk = gz.read(min(size - bytes_read, default.CHUNK_SIZE))
                        if not chunk:
                            break

                        bytes_read += len(chunk)

                        f.write(chunk)
                        checksum.update(chunk)

                        # callback for progress tracking
                        if cb:
                            cb(bytes_read)

                gz.close()

                # checksums from bytes read and meta data should match
                if checksum.hexdigest() != entry['checksum'][1]:
                    raise Exception('checksum mismatch: %s' % path)

            noffset = entry['noffset']

    def extract_all(self, extract_path, cb=None):
        for entry in self.meta['manifest']:
            self.extract(entry['path'], extract_path, cb=cb)

        members = [m['name'] for m in self.index_members()]
        for member in members:
            if self.tar:
                self.tar.extract(member, extract_path)
            else:
                shutil.copy(os.path.join(self.path, member), extract_path)

    def get_meta(self):
        reader = codecs.getreader('utf8')
        return json.load(reader(self.tar.extractfile(default.META_FILENAME)))

    def get_member(self, member):
        return self.meta[member]

    def list(self):
        return [tuple(e['path']) for e in self.meta['manifest']]

    def size_compressed(self):
        return self.meta[-1]['noffset']

    def index_members(self):
        if self.tar:
            return [{
                'size': m.size,
                'name': m.name,
            } for m in self.tar.getmembers() if m.name != default.ARCHIVE_FILENAME]
        else:
            return [{
                'size': os.stat(os.path.join(self.path, m)).st_size,
                'name': m,
            } for m in os.listdir(self.path) if m != default.ARCHIVE_FILENAME]

    def size(self):
        indices = [m['size'] for m in self.index_members()]
        files = [m['size'] for m in self.meta['manifest']]
        return sum(indices) + sum(files)
