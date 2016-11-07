from __future__ import print_function
import argparse, sys
import pip
from safety import safety, __version__
from safety.formatter import report


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='filenames to check')
    parser.parse_args(argv)

    packages = pip.get_installed_distributions()
    vulns = safety.check(packages=packages)

    if vulns:
        print('Safety version {} found security vulnerabilities:'.format(__version__))
        print(report(vulns=vulns, full=True))
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
