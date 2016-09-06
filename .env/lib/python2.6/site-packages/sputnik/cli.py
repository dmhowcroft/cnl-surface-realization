# pylint: disable=C0330
import argparse
import logging

from . import default
from . import install, build, remove, search, find, upload, update, files, purge


def set_log_level(args):
    level = getattr(logging, args.log_level.upper())
    logging.basicConfig(level=level)


def add_build_parser(subparsers):
    parser = subparsers.add_parser('build',
        help='build package from package.json')
    parser.add_argument('package_path',
        default=default.build_package_path,
        nargs='?',
        help='package.json directory')
    parser.add_argument('archive_path',
        nargs='?',
        help='archive path')

    def run(args):
        set_log_level(args)
        build(package_path=args.package_path,
              archive_path=args.archive_path)

    parser.set_defaults(run=run)


def add_install_parser(subparsers):
    parser = subparsers.add_parser('install',
        help='install package from repository or filesystem')
    parser.add_argument('package_name',
        help='package name or path')

    def run(args):
        set_log_level(args)
        install(app_name=args.name,
                app_version=args.version,
                package_name=args.package_name,
                data_path=args.data_path,
                repository_url=args.repository_url)

    parser.set_defaults(run=run)


def add_remove_parser(subparsers):
    parser = subparsers.add_parser('remove',
        help='remove installed package')
    parser.add_argument('package_string',
        help='package string')

    def run(args):
        set_log_level(args)
        remove(app_name=args.name,
               app_version=args.version,
               package_string=args.package_string,
               data_path=args.data_path)

    parser.set_defaults(run=run)


def add_find_parser(subparsers):
    parser = subparsers.add_parser('find',
        help='find installed packages')
    parser.add_argument('package_string',
        default=default.find_package_string,
        nargs="?",
        help='package string')
    parser.add_argument('--meta',
        default=default.find_meta,
        action='store_true',
        help='show package meta data')
    parser.add_argument('--cache',
        default=default.find_cache,
        action='store_true',
        help='find cached instead of installed packages')

    def run(args):
        set_log_level(args)
        find(app_name=args.name,
             app_version=args.version,
             package_string=args.package_string,
             meta=args.meta,
             cache=args.cache,
             data_path=args.data_path)

    parser.set_defaults(run=run)


def add_search_parser(subparsers):
    parser = subparsers.add_parser('search',
        help='search installable packages on repository')
    parser.add_argument('search_string',
        nargs="?",
        help='search string')

    def run(args):
        set_log_level(args)
        search(app_name=args.name,
               app_version=args.version,
               search_string=args.search_string,
               data_path=args.data_path,
               repository_url=args.repository_url)

    parser.set_defaults(run=run)


def add_upload_parser(subparsers):
    parser = subparsers.add_parser('upload',
        help='upload package')
    parser.add_argument('package_path',
        help='package path')

    def run(args):
        set_log_level(args)
        upload(app_name=args.name,
               app_version=args.version,
               package_path=args.package_path,
               data_path=args.data_path,
               repository_url=args.repository_url)

    parser.set_defaults(run=run)


def add_update_parser(subparsers):
    parser = subparsers.add_parser('update',
        help='update package cache')

    def run(args):
        set_log_level(args)
        update(app_name=args.name,
               app_version=args.version,
               data_path=args.data_path,
               repository_url=args.repository_url)

    parser.set_defaults(run=run)


def add_files_parser(subparsers):
    parser = subparsers.add_parser('files',
        help='displays package files')
    parser.add_argument('package_string',
        help='package string')

    def run(args):
        set_log_level(args)
        files(app_name=args.name,
              app_version=args.version,
              package_string=args.package_string,
              data_path=args.data_path)

    parser.set_defaults(run=run)


def add_purge_parser(subparsers):
    parser = subparsers.add_parser('purge',
        help='purges downloaded data')
    parser.add_argument('--cache',
        default=False,
        action='store_true',
        help='purge cache (cached packages)')
    parser.add_argument('--pool',
        default=False,
        action='store_true',
        help='purge pool (installed packages)')

    def run(args):
        set_log_level(args)
        purge(app_name=args.name,
              app_version=args.version,
              cache=args.cache,
              pool=args.pool,
              data_path=args.data_path)

    parser.set_defaults(run=run)


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name',
        help='app name')
    parser.add_argument('--version',
        help='app version')
    parser.add_argument('--data-path',
        help='data storage path')
    parser.add_argument('--repository-url',
        help='package repository path')
    parser.add_argument('--log-level',
        default='info',
        help='log level (default: info)')

    subparsers = parser.add_subparsers()
    add_build_parser(subparsers)
    add_install_parser(subparsers)
    add_remove_parser(subparsers)
    add_find_parser(subparsers)
    add_search_parser(subparsers)
    add_upload_parser(subparsers)
    add_update_parser(subparsers)
    add_files_parser(subparsers)
    add_purge_parser(subparsers)

    return parser
