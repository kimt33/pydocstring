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


# FIXME: awful api
def wrap(text, width=100, indent_level=0, tabsize=4, edges=('', ''),
         added_initial_indent='', added_subsequent_indent='', remove_first_indent=False, **kwargs):
    """Wrap a text with the given line length and indentations.

    Parameters
    ----------
    text : str
        Text that will be wrapped
    width : int
        Maximum number of characters allowed in each width
    indent_level : int
        Number of indents (tabs) that are needed for the docstring
    tabsize : int
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
    kwargs['tabsize'] = tabsize
    kwargs['width'] = width - len(edges[0]) - len(edges[1])

    tab = tabsize * indent_level * ' '
    kwargs['initial_indent'] = kwargs.setdefault('initial_indent', tab) + added_initial_indent
    kwargs['subsequent_indent'] = (kwargs.setdefault('subsequent_indent', tab)
                                   + added_subsequent_indent)

    default_kwargs = {'expand_tabs': True, 'replace_whitespace': False, 'drop_whitespace': True,
                      'break_long_words': False}
    default_kwargs.update(kwargs)

    lines = textwrap.fill(text, **default_kwargs).split('\n')
    if remove_first_indent:
        # find how much it was indented
        indent = re.search('^( *).', lines[0]).group(1)
        lines[0] = lines[0][len(indent):]

    output = [re.sub(r'^(\s*)(.+)$', r'\1{0}\2{1}'.format(*edges), line) for line in lines]
    return '\n'.join(output)
