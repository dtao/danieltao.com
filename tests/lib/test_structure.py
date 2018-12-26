import os

from datetime import date

from lib.structure import Directory
from tests import TEST_BASE_PATH


def test_directory():
    data = Directory(os.path.join(TEST_BASE_PATH, 'source')).as_dict()

    assert data == {
        'type': 'directory',
        'name': 'source',
        'path': '.',
        'entries': {
            'foo': {
                'type': 'directory',
                'name': 'foo',
                'path': 'foo',
                'entries': {
                    'bar.md': {
                        'type': 'file',
                        'name': 'bar.md',
                        'path': 'foo/bar.md',
                        'data': {
                            'title': 'Bar',
                            'date': date(2018, 12, 24)
                        },
                        'content': '<p>This is the content of bar.md.</p>\n'
                    }
                }
            },
            'baz.md': {
                'type': 'file',
                'name': 'baz.md',
                'path': 'baz.md',
                'data': {},
                'content': '<p>This is the content of baz.md.</p>\n'
            }
        }
    }
