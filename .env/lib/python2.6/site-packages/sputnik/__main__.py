import os
import sys

from . import cli


def main():
    parser = cli.get_parser()

    args = parser.parse_args(sys.argv[1:])
    if hasattr(args, 'run'):
        args.run(args)
    else:
        parser.print_usage()


def test():
    import pytest
    path = os.path.dirname(__file__)
    test_path = os.path.join(path, 'tests')
    pytest.main(sys.argv[2:] + [test_path])


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test()
    else:
        main()
