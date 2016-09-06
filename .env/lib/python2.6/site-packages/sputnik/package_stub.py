import io
import json
import contextlib
try:
    from types import TypeType as type
except ImportError:
    pass

import semver

from . import util


class PackageStub(object):
    keys = ['name', 'version', 'description', 'license', 'compatibility']

    def __init__(self, defaults=None):
        defaults = defaults or {}
        for key in self.keys:
            setattr(self, key, defaults.get(key))

    def is_valid(self, raise_exception=False):
        res = False
        if self.name and self.version:
            res = True

        if raise_exception and not res:
            raise Exception('invalid package')
        return res

    @property
    def ident(self):
        if self.is_valid(True):
            return util.archive_filename(self.name, self.version)

    def to_json(self, keys=None):
        return util.json_dump(self.to_dict(keys))

    def to_dict(self, keys=None):
        keys = keys or []
        if hasattr(self, 'is_valid'):
            self.is_valid()
        return dict([
            (k, getattr(self, k))
            for k in self.keys
            if not keys or k in keys])

    def has_file(self, *path_parts):
        raise NotImplementedError

    def file_path(self, *path_parts):
        raise NotImplementedError

    def dir_path(self, *path_parts):
        raise NotImplementedError

    @contextlib.contextmanager
    def open(self, path_parts, mode='r', encoding='utf8', default=IOError):
        if self.has_file(*path_parts):
            f = io.open(self.file_path(*path_parts),
                        mode=mode, encoding=encoding)
            yield f
            f.close()

        else:
            if isinstance(default, type) and issubclass(default, Exception):
                raise default(self.file_path(*path_parts))
            elif isinstance(default, Exception):
                raise default
            else:
                yield default

    def load_json(self, path_parts, mode='r', encoding='utf8', default=IOError):
        if self.has_file(*path_parts):
            with io.open(self.file_path(*path_parts),
                         mode=mode, encoding=encoding) as f:
                return json.load(f)

        else:
            if isinstance(default, type) and issubclass(default, Exception):
                raise default(self.file_path(*path_parts))
            elif isinstance(default, Exception):
                raise default
            else:
                return default

    def _error_on_different_name(self, other):
        if self.name != other.name:
            raise Exception('name mismatch: %s != %s' % (self.name, other.name))

    def __gt__(self, other):
        self._error_on_different_name(other)
        return semver.compare(self.version, other.version) > 0

    def __lt__(self, other):
        self._error_on_different_name(other)
        return semver.compare(self.version, other.version) < 0

    def __eq__(self, other):
        self._error_on_different_name(other)
        return semver.compare(self.version, other.version) == 0

    def __ne__(self, other):
        return not self.__eq__(other)

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)
