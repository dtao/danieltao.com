import re

import commonmark
import yaml

divider = re.compile(r'^---$', re.MULTILINE)


def parse_markdown_with_frontmatter(content):
    sections = [section.strip() for section in divider.split(content)
                if section.strip() != '']

    if len(sections) > 2:
        raise ValueError('There should be 2 sections: the frontmatter and '
                         'the content.')

    # Allow for frontmatter to be omitted.
    if len(sections) == 1:
        frontmatter = ''
        content = sections[0]
    else:
        frontmatter, content = sections

    return {
        'frontmatter': yaml.load(frontmatter),
        'content': content,
        'html': commonmark.commonmark(content)
    }
