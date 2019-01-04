import os
import sys

from lib.build import build_site

if __name__ == '__main__':

    if len(sys.argv) >= 2:
        source_path = sys.argv[1]
    else:
        source_path = os.path.join(os.getcwd(), 'source')

    if len(sys.argv) >= 3:
        dest_path = sys.argv[2]
    else:
        dest_path = os.path.join(os.getcwd(), 'dest')

    build_site(source_path, dest_path)
