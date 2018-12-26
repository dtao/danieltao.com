import os
import subprocess

from lib.structure import Directory
from tests import TEST_BASE_PATH


def test_build():
    # Build tests/source
    source_path = os.path.join(TEST_BASE_PATH, 'source')
    dest_path = os.path.join(TEST_BASE_PATH, 'dest')
    Directory(source_path).build(dest_path)

    # Leverage git to detect changes
    diff = subprocess.check_output(
        ['git', 'diff', os.path.relpath(dest_path, os.getcwd())])

    # Ensure no changes have been introduced
    assert len(diff) == 0
