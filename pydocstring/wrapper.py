import inspect
from functools import wraps
from pydocstring.docstring import Docstring
from pydocstring.numpy_docstring import parse_numpy
from pydocstring.utils import extract_members


def kwarg_wrapper(wrapper):
    """Wraps the keyword arguments into the wrapper.

    The wrapper behaves differently when used as a decorator if the arguments are given. i.e.
    @decorator vs @decorator(). Therefore, the default keyword values of the wrapper must be changed
    (with another wrapper).
    """
    @wraps(wrapper)
    def new_wrapper(obj=None, **kwargs):
        """Reconstruction of the provided wrapper so that keyword arguments are rewritten.

        When a wrapper is used as a decorator and is not called (i.e. no parenthesis),
        then the wrapee (wrapped object) is automatically passed into the decorator. This function
        changes the "default" keyword arguments so that the decorator is not called (so that the
        wrapped object is automatically passed in). If the decorator is called,
        e.g. `x = decorator(x)`, then it simply needs to return the wrapped value.
        """
        # the decorator is evaluated.
        if obj is None and len(kwargs) > 0:
            # Since no object is provided, we need to turn the wrapper back into a form so that it
            # will automatically pass in the object (i.e. turn it into a function) after overwriting
            # the keyword arguments
            return lambda orig_obj: wrapper(orig_obj, **kwargs)
        else:
            # Here, the object is provided OR keyword argument is not provided.
            # If the object is provided, then the wrapper can be executed.
            # If the object is not provided and keyword argument is not provided, then an error will
            # be raised.
            return wrapper(obj, **kwargs)

    return new_wrapper


# TODO: check that docstring is parsed properly
@kwarg_wrapper
def docstring(obj, style='numpy', width=100, indent_level=0, tabsize=4, is_raw=False):
    """Wrapper for converting docstring of an object from one format to another.

    Parameters
    ----------
    obj : function, module, class
        Object that contains a docstring.
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
    # because attributes of property cannot be set
    if not isinstance(obj, property):
        obj._docstring = doc

    return obj


@kwarg_wrapper
def docstring_recursive(obj, style='numpy', width=100, indent_level=0, tabsize=4, is_raw=False):
    """Wrapper for recursively converting docstrings within an object from one format to another.

    This wrapper recursively converts every member of the object (and their members) if their
    source code is located in the same file.

    Parameters
    ----------
    obj : function, module, class
        Object that contains a docstring.
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
    obj = docstring(obj, style=style, width=width, indent_level=indent_level, tabsize=tabsize,
                    is_raw=is_raw)

    # property
    if isinstance(obj, property):
        return obj

    # wrap members
    members = extract_members(obj, recursive=False)
    for name in members.keys():
        # apply wrapper docstring to member
        inner_obj = docstring(getattr(obj, name), style=style, width=width,
                              indent_level=indent_level+1, tabsize=tabsize, is_raw=is_raw)
        # recurse for all members of member
        inner_obj = docstring_recursive(inner_obj, style=style, width=width,
                                        indent_level=indent_level+1, tabsize=tabsize, is_raw=is_raw)
        # set new member
        setattr(obj, name, inner_obj)

    return obj
