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
def wrap(text, width=100, indent_level=0, tabsize=4, edges=('', ''), added_indent='',
         remove_initial_indent=False, **kwargs):
    """Wrap a text with the given line length and indentations.

    Parameters
    ----------
    text : str
        Text that will be wrapped
    width : int
        Maximum number of characters allowed in each line
    indent_level : int
        Number of indents (tabs) that are needed for the docstring
    tabsize : int
        Number of spaces that corresponds to a tab
    edges : 2-tuple of string
        Beginning and end of each line (after indent).
    added_indent : str, 2-tuple/list of str
        Indentation to be added after the indentation by the levels.
        If 2 strings are given, then first string corresponds to the initial indent and the second
        string to the subsequent indents.
        Default is no added indent.
    remove_initial_indent : bool
        Flag for removing the indentation on the first line.
    kwargs : dict
        Other options for the textwrap.fill.
        Default replaces tabs with spaces ('expand_tabs': True), does not replace whitespace
        ('replace_whitespace': False), drops whitespaces (that are not indentations) before or after
        sentences ('drop_whitespace': True), and does not break long word into smaller pieces
        ('break_long_words': False).
    """
    # default
    kwargs.setdefault('expand_tabs', True)
    kwargs.setdefault('replace_whitespace', False)
    kwargs.setdefault('drop_whitespace', tuple(edges) == ('', ''))
    kwargs.setdefault('break_long_words', False)

    # parameters
    kwargs['tabsize'] = tabsize
    kwargs['width'] = width - len(edges[0]) - len(edges[1])

    if isinstance(added_indent, str):
        added_indent = [added_indent]
    if isinstance(added_indent, (list, tuple)) and len(added_indent) == 1:
        added_indent *= 2
    elif len(added_indent) > 2:
        raise ValueError('`added_indent` must be given as a string or a list/tuple of at most two '
                         'strings, where the first string correspond to the initial and the second '
                         'correspond to the subsequent indents. If only one string is given, then '
                         'all lines are indented.')

    tab = tabsize * indent_level * ' '
    kwargs['initial_indent'] = kwargs.setdefault('initial_indent', tab) + added_indent[0]
    kwargs['subsequent_indent'] = kwargs.setdefault('subsequent_indent', tab) + added_indent[1]
    num_indent = [len(kwargs['initial_indent']), len(kwargs['subsequent_indent'])]

    lines = textwrap.fill(text, **kwargs).split('\n')
    if remove_initial_indent:
        # remove the initial indent
        lines[0] = lines[0][num_indent[0]:]
        num_indent[0] = 0

    # add edges
    output = [re.sub(r'^({0})(.+)$'.format(' ' * num_indent[0]),
                     r'\1{0}\2{1}'.format(*edges),
                     lines[0])]
    output += [re.sub(r'^({0})(.+)$'.format(' ' * num_indent[1]),
                      r'\1{0}\2{1}'.format(*edges),
                      line) for line in lines[1:]]
    return '\n'.join(output)
