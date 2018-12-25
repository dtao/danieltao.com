import os
import re
import sys

import pystache

from lib.structure import read_directory

if len(sys.argv) >= 2:
    source_path = sys.argv[1]
else:
    source_path = os.path.join(os.getcwd(), 'source')

if len(sys.argv) >= 3:
    dest_path = sys.argv[2]
else:
    dest_path = os.path.join(os.getcwd(), 'dest')


def build_entries(entries):
    for entry in entries:
        os.makedirs(os.path.join(dest_path, os.path.dirname(entry['path'])),
                    exist_ok=True)

        if entry['type'] == 'directory':
            build_entries(entry['entries'])

        elif entry['type'] == 'file' and entry['name'] != '__template__.html':
            output_path = os.path.join(dest_path, entry['path'])

            if entry['name'].endswith('.md'):
                output_path = re.sub(r'\.md$', '.html', output_path)
                template_path = os.path.join(source_path,
                                             os.path.dirname(entry['path']),
                                             '__template__.html')
                with open(template_path, 'r') as f:
                    template = f.read()
            else:
                template = entry['content']

            with open(output_path, 'w') as f:
                f.write(pystache.render(template, entry))

source_data = read_directory(source_path)
build_entries(source_data['entries'])
