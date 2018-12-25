import os

from datetime import date

from lib.structure import read_directory
from tests import TEST_BASE_PATH


def test_read_directory():
    data = read_directory(os.path.join(TEST_BASE_PATH, 'source'))

    assert data['type'] == 'directory'
    assert data['name'] == 'source'
    assert data['path'] == '.'

    assert len(data['entries']) == 2

    foo_data = next(entry for entry in data['entries']
                    if entry['name'] == 'foo')
    assert foo_data == {
        'type': 'directory',
        'name': 'foo',
        'path': 'foo',
        'entries': [
            {
                'type': 'file',
                'name': 'bar.md',
                'path': 'foo/bar.md',
                'data': {
                    'title': 'Bar',
                    'date': date(2018, 12, 24)
                },
                'content': 'This is the content of bar.md.'
            }
        ]
    }

    baz_data = next(entry for entry in data['entries']
                    if entry['name'] == 'baz.md')
    assert baz_data == {
        'type': 'file',
        'name': 'baz.md',
        'path': 'baz.md',
        'data': {},
        'content': 'This is the content of baz.md.'
    }
