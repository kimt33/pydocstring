from pydocstring.docstring import Docstring
from pydocstring.numpy_docstring import parse_numpy
from pydocstring.utils import extract_members


def docstring(obj, style='numpy', width=100, indent_level=0, tabsize=4, is_raw=False):
    """Wrapper for converting docstring of an object from one format to another.

    Parameters
    ----------
    obj : str, pydocstring.docstring.Docstring
        Docstring that will be converted.
    style : {'numpy', 'google', str}
        Style of the docstring.
    width : int
        Maximum number of characters allowed in each width
    indent_level : int
        Number of indents (tabs) that are needed for the docstring
    tabsize : int
        Number of spaces that corresponds to a tab
    is_raw : bool
        True if the generated numpy documentation string is a raw string. Docstring should be
        raw when backslash is used (e.g. math equations).
        Default is False.

    Raises
    ------
    TypeError
        If the obj's __doc__ is neither str nor Docstring instance.
    NotImplementedError
        If `style` is not 'numpy'
    """
    if style == 'numpy':
        doc = Docstring(**parse_numpy(obj.__doc__, contains_quotes=False))
    elif style == 'code':
        doc = obj.__doc__
    else:
        raise NotImplementedError('Only numpy and code (Docstring instance) style are supported at '
                                  'the moment.')
    # over write docstring
    obj.__doc__ = doc.make_numpy(width=width, indent_level=indent_level, tabsize=tabsize,
                                 is_raw=is_raw, include_quotes=False)
    # store Docstring instance
    obj._docstring = doc

    return obj


def docstring_recursive(obj, style='numpy', width=100, indent_level=0, tabsize=4, is_raw=False):
    """Wrapper for recursively converting docstrings within an object from one format to another.

    This wrapper recursively converts every member of the object (and their members) if their
    source code is located in the same file.

    Parameters
    ----------
    obj : str, pydocstring.docstring.Docstring
        Docstring that will be converted.
    style : {'numpy', 'google', str}
        Style of the docstring.
    width : int
        Maximum number of characters allowed in each width.
    indent_level : int
        Number of indents (tabs) that are needed for the docstring.
    tabsize : int
        Number of spaces that corresponds to a tab.
    is_raw : bool
        True if the generated numpy documentation string is a raw string. Docstring should be
        raw when backslash is used (e.g. math equations).
        Default is False.

    Raises
    ------
    TypeError
        If the obj's __doc__ is neither str nor Docstring instance.
    NotImplementedError
        If `style` is not 'numpy'.

    Returns
    -------
    obj
        Wrapped object where the docstring is in the selected format and the corresponding Docstring
        instance is stored in `_docstring`.
    """
    # wrap self
    obj = docstring(obj, style='numpy', width=width, indent_level=indent_level, tabsize=tabsize,
                    is_raw=is_raw)

    # wrap members
    members = extract_members(obj, recursive=False)
    for name in members.keys():
        # apply wrapper docstring to member
        inner_obj = docstring(getattr(obj, name), style='numpy', width=width,
                              indent_level=indent_level, tabsize=tabsize, is_raw=is_raw)
        # recurse for all members of member
        inner_obj = docstring_recursive(inner_obj, style='numpy', width=width,
                                        indent_level=indent_level, tabsize=tabsize, is_raw=is_raw)
        # set new member
        setattr(obj, name, inner_obj)

    return obj
