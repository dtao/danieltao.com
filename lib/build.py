import os

from lib.structure import Directory


def build_site(source_path, dest_path=None):
    dest_path = dest_path or os.path.join(source_path, '..', 'dest')
    Directory(source_path).build(dest_path)


if __name__ == '__main__':
    import sys

    if len(sys.argv) >= 2:
        source_path = sys.argv[1]
    else:
        source_path = os.path.join(os.getcwd(), 'source')

    if len(sys.argv) >= 3:
        dest_path = sys.argv[2]
    else:
        dest_path = os.path.join(os.getcwd(), 'dest')

    build_site(source_path, dest_path)
