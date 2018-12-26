import os
import re

from jinja2 import Template

from lib.parse import parse_markdown_with_frontmatter


class Entry(object):
    def __init__(self, path, parent=None):
        self.abs_path = path
        self.parent = parent
        self.root = parent.root if parent else self
        self.name = os.path.basename(path)

    @property
    def base_path(self):
        return self.root.abs_path

    @property
    def path(self):
        return os.path.relpath(self.abs_path, self.base_path)


class Directory(Entry):
    dict_keys = ('type', 'name', 'path', 'entries')

    def __init__(self, *args, **kwargs):
        self.type = 'directory'
        super().__init__(*args, **kwargs)
        self._entries = {}
        self._populated = False

    @property
    def entries(self):
        if self._populated:
            for entry in self._entries.values():
                yield entry

        with os.scandir(self.abs_path) as scanned_entries:
            for entry in scanned_entries:
                if entry.is_file():
                    file = File(entry.path, self)
                    self._entries[file.path] = file
                    yield file
                else:
                    directory = Directory(entry.path, self)
                    self._entries[directory.path] = directory
                    yield directory
            self._populated = True

    @property
    def template(self):
        if not hasattr(self, '_template'):
            template_path = os.path.join(self.abs_path, '__template__.html')
            if os.path.isfile(template_path):
                with open(template_path, 'r') as f:
                    self._template = Template(f.read())
            else:
                self._template = self.parent.template
        return self._template

    @property
    def directories(self):
        return (entry for entry in self.entries if entry.type == 'directory')

    @property
    def files(self):
        return (entry for entry in self.entries
                if entry.type == 'file' and entry.name != '__template__.html')

    def entry(self, path):
        self._populate()
        return self._entries[path]

    def build(self, dest_path):
        os.makedirs(os.path.join(dest_path, self.path), exist_ok=True)
        for file in self.files:
            file.build(dest_path)
        for directory in self.directories:
            directory.build(dest_path)

    def as_dict(self):
        return {
            'type': 'directory',
            'name': self.name,
            'path': self.path,
            'entries': {
                e.name: e.as_dict()
                for e in self.entries
            }
        }

    def _populate(self):
        if self._populated:
            return

        list(self.entries)


class File(Entry):
    def __init__(self, *args, **kwargs):
        self.type = 'file'
        super().__init__(*args ,**kwargs)
        self._data = {}
        self._content = None
        self._populated = False

    @property
    def dest_path(self):
        return re.sub(r'\.md$', '.html', self.path)

    @property
    def data(self):
        self._populate()
        return self._data

    @property
    def content(self):
        self._populate()
        return self._content

    def build(self, dest_path):
        if self.name == '__template__.html':
            return

        output_path = os.path.join(dest_path, self.path)

        if self.name.endswith('.md'):
            output_path = re.sub(r'\.md$', '.html', output_path)
            template = self.parent.template
        else:
            template = Template(self.content)

        with open(output_path, 'w') as f:
            f.write(template.render(site=self.root, page=self))

    def as_dict(self):
        return {
            k: getattr(self, k)
            for k in ('type', 'name', 'path', 'data', 'content')
        }

    def _populate(self):
        if self._populated:
            return

        with open(self.abs_path, 'r') as f:
            content = f.read()

        if self.abs_path.endswith('.md'):
            parsed_file = parse_markdown_with_frontmatter(content)
            self._data = parsed_file['frontmatter'] or {}
            self._content = parsed_file['html']
        else:
            self._content = content

        self._populated = True
