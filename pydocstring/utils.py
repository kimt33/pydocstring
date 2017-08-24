import re
# FIXME: remove textwrap dependency and code from scratch
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


# FIXME: bug. see test
# FIXME: add examples, make doc better
def layered_wrap(dict_edges_contents, width=100, indent_level=0, tabsize=4, edges=("'", "'"),
                 added_indent='', remove_initial_indent=False, **kwargs):
    """Recursively wraps the content of a layer with the appropriate edges.

    When making nicely indented multiline nested lists, appropriate edges, e.g. [ and ], are used
    to contain the contents inside. The contents inside can be indented and can also be encased in
    edges.

    Parameters
    ----------
    dict_edges_contents : dict
        Dictionary of the edges to the contents of the edges.
        Each dictionary must specify exactly one key/value.
        The key is 3-tuple of the edge on the left and the right and whether the next content will
        start from a newline (vs current line).
        The value is a string, list of strings, or another dictionary (or list of dictionaries) that
        will be nested inside the current layer.
    width : int
        Maximum number of characters allowed in each width.
    indent_level : int
        Number of indents (tabs) that are needed for the docstring.
    tabsize : int
        Number of spaces that corresponds to a tab
    edges : 2-tuple of string
        Beginning and end of each line (after indent).
    added_indent : str, 2-tuple/list of str
        Indentation to be added after the indentation via `indent_level`.
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

    Raises
    ------
    TypeError
        If `dict_edges_contents` is not a dictionary.
    ValueError
        If `dict_edges_contents` has more than one key/value.
        If value of `dict_edges_contents` is not a dictionary, string, or list/tuple of dictionaries
        and strings.
        If `layers_text` does not have the same shape as the `layers_edges`
    """
    # NOTE: i would love to use numpy here, but that would mean adding a dependency solely for shape
    #       checking... So recursion will be used.
    if not isinstance(dict_edges_contents, dict):
        raise TypeError('`dict_edges_contents` must be a dictionary.')

    if len(dict_edges_contents) != 1:
        raise ValueError('`dict_edges_contents` must have exactly one key/value.')

    kwargs['tabsize'] = tabsize

    (l_edge, r_edge, has_newline), layer = dict_edges_contents.popitem()
    wrapped_l_edge = wrap(l_edge, width=width, indent_level=indent_level,
                          drop_whitespace=False, **kwargs)
    wrapped_r_edge = wrap(r_edge, width=width, indent_level=indent_level if has_newline else 0,
                          drop_whitespace=False, **kwargs)

    if isinstance(layer, dict) or isinstance(layer, str):
        layer = [layer]
    elif not isinstance(layer, (list, tuple)):
        raise ValueError('Contents of `dict_edges_contents` must be a dictionary, string, or '
                         'list/tuple of dictionaries and strings.')

    output = ''
    output += wrapped_l_edge
    if has_newline:
        output += '\n'
    for i, item in enumerate(layer):
        if isinstance(item, dict):
            if has_newline:
                output += layered_wrap(item,
                                       width=width,
                                       indent_level=indent_level+1,
                                       added_indent=added_indent,
                                       remove_initial_indent=False,
                                       **kwargs)
            else:
                output += layered_wrap(item,
                                       width=width - len(r_edge) - len(l_edge),
                                       indent_level=indent_level,
                                       added_indent=' ' * len(l_edge),
                                       remove_initial_indent=True,
                                       **kwargs)

        elif isinstance(item, str):
            if has_newline:
                output += wrap(item,
                               width=width,
                               indent_level=indent_level+1,
                               edges=edges,
                               added_indent='',
                               remove_initial_indent=False,
                               **kwargs)
            else:
                output += wrap(item,
                               width=width,
                               indent_level=0,
                               edges=edges,
                               added_indent=' '*len(wrapped_l_edge),
                               remove_initial_indent=True,
                               **kwargs)
        else:
            raise ValueError('Contents of `dict_edges_contents` must be a dictionary, string, or '
                            'list/tuple of dictionaries and strings.')
        if i != len(layer) - 1:
            if has_newline:
                output += ',\n'
            else:
                output += ', '
    if has_newline:
        output += '\n'
    output += wrapped_r_edge

    return output
