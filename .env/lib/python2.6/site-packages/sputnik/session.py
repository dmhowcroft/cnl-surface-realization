import os
import codecs
import json
try:
    from http.cookiejar import MozillaCookieJar
except ImportError:
    from cookielib import MozillaCookieJar
try:
    from urllib.request import Request, build_opener, HTTPRedirectHandler, HTTPCookieProcessor
except ImportError:
    from urllib2 import Request, build_opener, HTTPRedirectHandler, HTTPCookieProcessor

from . import default
from . import util


class Session(object):
    def __init__(self, app_name, app_version, data_path, **kwargs):
        self.app_name = app_name
        self.app_version = app_version

        if not data_path or not os.path.isdir(data_path):
            raise Exception('invalid data_path: %s' % data_path)

        self.cookie_jar = MozillaCookieJar(os.path.join(data_path, default.COOKIES_FILENAME))
        try:
            self.cookie_jar.load()
        except EnvironmentError:
            pass

        self.opener = build_opener(
            HTTPRedirectHandler(),
            HTTPCookieProcessor(self.cookie_jar))

        super(Session, self).__init__(**kwargs)

    def open(self, request, default_charset=None):
        request.add_header('User-Agent', util.user_agent(self.app_name, self.app_version))

        system_string = json.dumps(util.system_info(self.app_name, self.app_version))
        request.add_header('X-Sputnik-System', system_string)

        r = self.opener.open(request)

        if hasattr(r.headers, 'get_content_charset'):  # py3
            charset = r.headers.get_content_charset() or default_charset
        elif hasattr(r.headers, 'getparam'):  # py2
            charset = r.headers.getparam('charset') or default_charset
        else:
            charset = default_charset

        if charset is None:
            return r
        return codecs.getreader(charset)(r)

    def __del__(self):
        if hasattr(self, 'cookie_jar'):
            self.cookie_jar.save()


class GetRequest(Request):
    pass


class HeadRequest(Request):
    def get_method(self):
        return 'HEAD'


class PutRequest(Request):
    def get_method(self):
        return 'PUT'
