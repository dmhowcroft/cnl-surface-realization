import os
import json
import hashlib
import time
import logging
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from . import util
from .archive import Archive
from .session import Session, GetRequest, PutRequest
from .cache import Cache
from .package_stub import PackageStub


class Index(object):
    def __init__(self, app_name, app_version, data_path, repository_url, **kwargs):
        self.logger = logging.getLogger(__name__)

        self.app_name = app_name
        self.app_version = app_version

        if not repository_url:
            raise Exception('invalid repository_url: %s' % repository_url)

        self.data_path = data_path
        self.repository_url = repository_url

        super(Index, self).__init__(**kwargs)

    def upload(self, path):
        from boto.s3.connection import S3Connection

        access_key_id = os.environ['AWS_ACCESS_KEY_ID']
        secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
        os.environ['S3_USE_SIGV4'] = 'True'

        # get aws/s3 upload information
        session = Session(self.app_name, self.app_version, self.data_path)
        url = urljoin(self.repository_url, '/upload')
        request = GetRequest(url)
        response = session.open(request, 'utf8')
        result = json.load(response)

        conn = S3Connection(access_key_id, secret_access_key,
                            host='s3.%s.amazonaws.com' % result['region'])
        bucket = conn.get_bucket(result['bucket'], validate=False)

        # to allow random access we upload each archive member individually
        archive = Archive(path)
        for key_name, f in archive.fileobjs().items():
            self.logger.info('preparing upload for %s', key_name)
            headers = {
                util.s3_header('md5'): hashlib.md5(f.read()).hexdigest()
            }
            f.seek(os.SEEK_SET, 0)

            self.logger.info('uploading %s...', key_name)
            key = bucket.new_key(key_name)
            key.set_contents_from_file(f, headers=headers)

        # without reindexing the index server wouldn't know that we
        # uploaded a new package
        request = PutRequest(urljoin(self.repository_url, '/reindex'))
        response = session.open(request)

        res = response.getcode() == 200
        self.logger.info('reindex %s', res)
        return res

    def update(self, max_retries=5):
        if max_retries <= 0:
            raise Exception('index server out of sync')

        request = GetRequest(urljoin(self.repository_url, '/models'))
        session = Session(self.app_name, self.app_version, self.data_path)
        cache = Cache(self.app_name, self.app_version, self.data_path)

        # remember cached packages for removal
        packages = cache.find()

        index = json.load(session.open(request, 'utf8'))

        for ident, (meta_url, etag) in index.items():
            if not cache.exists(ident, etag):
                url = urljoin(self.repository_url, meta_url)
                request = GetRequest(url)
                response = session.open(request, 'utf8')
                meta = json.load(response)

                package = PackageStub(meta['package'])
                assert ident == package.ident

                # index server's etag should match s3's etag
                if util.unquote(response.headers['etag']) != etag:
                    self.logger.info('wait for index server to sync')
                    time.sleep(3)
                    return self.update(max_retries - 1)

                assert util.unquote(response.headers['etag']) == etag
                cache.update(meta, url=url, etag=etag)

            # shrink list by one
            packages = [p for p in packages if p.ident != ident]

        # remove leftovers
        for package in packages:
            package.remove()
