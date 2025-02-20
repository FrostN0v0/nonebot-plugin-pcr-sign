import sys


def main(*args):
    from ..cli import pcr

    pcr.main(*(["nb pcr"] + list(args or sys.argv[1:])))
