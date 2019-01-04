import os

from lib.structure import Directory


def build_site(source_path, dest_path=None):
    dest_path = dest_path or os.path.join(source_path, '..', 'dest')
    Directory(source_path).build(dest_path)
