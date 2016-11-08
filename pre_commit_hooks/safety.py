from __future__ import print_function
import sys
from safety.cli import check


def main(argv=None):
    try:
        check.main(['--full-report', '-r'] + argv)
    except SystemExit as error:
        if error.code == 0:
            return 0
        return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
