# The Plan

So here's my plan. I'll build a static site generator tool that does exactly
what I want, then I'll extract that out into its own library.

## How it will work, maybe

Take everything in source and treat that as input data. The data will map
directly to the files in source.

Directories will look like:

```
{
    "name": "source",
    "path": "source",
    "entries": []
}
```

Files will look like:

```
{
    "name": "foo",
    "path": "source/foo",
    "data": {
        "title": "Foo",
        "date": 2018-12-24
    },
    "content": "content of 'foo'"
}
```

The properties `name`, `path`, and `content` will come directly from the file
name, path, and content. The `data` property will come from the frontmatter at
the top of the file (only applicable for Markdown files).

The structure of the output needs to be defined somewhere. For now, how about a
file called **structure.yml**.
