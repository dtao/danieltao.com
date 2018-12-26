import os
import sys

from lib.structure import Directory

if len(sys.argv) >= 2:
    source_path = sys.argv[1]
else:
    source_path = os.path.join(os.getcwd(), 'source')

if len(sys.argv) >= 3:
    dest_path = sys.argv[2]
else:
    dest_path = os.path.join(os.getcwd(), 'dest')


Directory(source_path).build(dest_path)
