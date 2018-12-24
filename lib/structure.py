import os

from lib.parse import parse_markdown_with_frontmatter


def read_directory(path, base_path=None):
    base_path = base_path or os.path.dirname(path)
    base_name = os.path.basename(path)

    entries = []

    directory = {
        'type': 'directory',
        'name': base_name,
        'path': os.path.relpath(path, base_path),
        'entries': entries
    }

    with os.scandir(path) as scanned_entries:
        for entry in scanned_entries:
            if entry.is_file():
                entries.append(read_file(entry.path, base_path))
            else:
                entries.append(read_directory(entry.path, base_path))

    return directory


def read_file(path, base_path):
    data = {}

    with open(path, 'r') as f:
        content = f.read()

    if path.endswith('.md'):
        parsed_file = parse_markdown_with_frontmatter(content)
        data = parsed_file['frontmatter'] or {}
        content = parsed_file['content']

    return {
        'type': 'file',
        'name': os.path.basename(path),
        'path': os.path.relpath(path, base_path),
        'data': data,
        'content': content
    }
