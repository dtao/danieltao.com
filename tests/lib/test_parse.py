from textwrap import dedent

from lib.parse import parse_markdown_with_frontmatter


def test_parse_markdown_with_frontmatter():
    content = dedent('''
        ---
        foo: 1
        bar: 2
        ---

        This is some content.
    ''')

    result = parse_markdown_with_frontmatter(content)

    assert result['frontmatter'] == {
        'foo': 1,
        'bar': 2
    }

    assert result['content'] == 'This is some content.'

    assert result['html'] == '<p>This is some content.</p>\n'
