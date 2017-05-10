"""
Mucro
=====
"""
import argparse
import os
import sys
import textwrap
import shutil
import stat


__version__ = '2017.5.1'


def make_executable(path):
    # http://stackoverflow.com/a/30463972/170656
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2    # copy R bits to X
    os.chmod(path, mode)


def main(args: argparse.Namespace):
    contents = textwrap.dedent('''\
    #!/usr/bin/env bash
    "{}" "{}" "$@"
    ''')
    contents = contents.format(
        shutil.which('python'),
        os.path.abspath(args.pyfile)
    )

    with open(args.wrapper, 'w+') as f:
        f.write(contents)
        wrapper = os.path.abspath(args.wrapper)
    make_executable(wrapper)

    sym = os.path.join(args.bindir, args.wrapper)
    os.symlink(wrapper, sym)

    uninstaller = os.path.abspath(args.wrapper + '-uninstall')
    with open(uninstaller, 'w+') as f:
        for item in (sym, wrapper, uninstaller):
            f.write('rm "%s"\n' % item)
    make_executable(uninstaller)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--pyfile',
        help='Python script to wrap',
        required=True
    )
    parser.add_argument(
        '--wrapper',
        help='Name of the new shell script to be created.',
        required=True
    )
    parser.add_argument(
        '--bindir',
        help='Destination of the symlink',
        required=True
    )
    args = parser.parse_args()
    main(args)
