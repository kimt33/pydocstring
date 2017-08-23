import re
import textwrap


def remove_indent(text, include_firstline=False):
    """Removes leading whitespace from the provided text.

    Removes largest amount of leading whitespaces that is shared amongst all of the selected lines.

    Parameters
    ----------
    text : str or list of str
        Text from which the indents will be removed
    include_firstline : bool
        True if indents of the first line is also included
        Default is False

    Returns
    -------
    dedented_text : str
        Text after the indents are removed.

    Examples
    --------
    >>> remove_indent(''' abc
    ... de
    ...   fg''', include_firstline=True)
    'abc\nde\n  fg'
    >>> remove_indent(''' abc
    ... de
    ...   fg''', include_firstline=False)
    ' abc\nde\n  fg'
    """
    if isinstance(text, str):
        text = text.split('\n')
    if include_firstline:
        return textwrap.dedent('\n'.join(text))
    else:
        return '{0}\n{1}'.format(text[0], textwrap.dedent('\n'.join(text[1:])))


def wrap(text, line_length=100, indent_level=0, tab_width=4, edges=('', ''),
         added_initial_indent='', added_subsequent_indent='', **kwargs):
    """Wrap a text with the given line length and indentations.

    Parameters
    ----------
    text : str
        Text that will be wrapped
    line_length : int
        Maximum number of characters allowed in each width
    indent_level : int
        Number of indents (tabs) that are needed for the docstring
    tab_width : int
        Number of spaces that corresponds to a tab
    edges : 2-tuple of string
        Beginning and end of each sentence.
    kwargs : dict
        Other options for the textwrap.fill.
        Default replaces tabs with spaces ('expand_tabs': True), does not replace whitespace
        ('replace_whitespace': False), drops whitespaces (that are not indentations) before or after
        sentences ('drop_whitespace': True), and does not break long word into smaller pieces
        ('break_long_words': False).
    """
    default_kwargs = {'expand_tabs': True, 'replace_whitespace': False, 'drop_whitespace': True,
                      'break_long_words': False}
    default_kwargs.update(kwargs)

    tab = tab_width * indent_level * ' '
    initial_indent = tab + added_initial_indent
    subsequent_indent = tab + added_subsequent_indent
    text = textwrap.fill(text, initial_indent=initial_indent, subsequent_indent=subsequent_indent,
                         tabsize=tab_width, width=line_length - len(edges[0]) - len(edges[1]),
                         **default_kwargs)
    lines = text.split('\n')

    output = [re.sub(r'^(\s*)(.+)$', r'\1{0}\2{1}'.format(*edges), line) for line in lines]
    return '\n'.join(output)
