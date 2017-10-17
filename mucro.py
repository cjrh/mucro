"""
Mucro
=====
"""
import argparse
import os
import textwrap
import shutil


__version__ = '2017.10.1'


def make_executable(path):
    # http://stackoverflow.com/a/30463972/170656
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2    # copy R bits to X
    os.chmod(path, mode)


def main(args):
    contents = textwrap.dedent('''\
    #!/usr/bin/env bash
    "{}" "{}" "$@"
    ''')
    contents = contents.format(
        shutil.which('python'),
        os.path.abspath(args.pyfile)
    )

    if not args.wrapper:
        args.wrapper = os.path.splitext(
            os.path.basename(
                args.pyfile
            )
        )[0]

    sym = os.path.join(os.path.abspath(args.bindir), args.wrapper)
    if os.path.exists(sym):
        raise EnvironmentError(
            'Desired symlink already exists in "{}". Aborting'.format(
                args.bindir
            )
        )

    with open(args.wrapper, 'w+') as f:
        f.write(contents)
        wrapper = os.path.abspath(args.wrapper)
    make_executable(wrapper)
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
        help=('Name of the new shell script to be created. If '
              'not provided, the filename component of the --pyfile '
              'option will be used, without the .py extension.'),
        default=None
    )
    parser.add_argument(
        '--bindir',
        help='Destination of the symlink',
        required=True
    )
    args = parser.parse_args()
    main(args)
