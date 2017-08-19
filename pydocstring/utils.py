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

