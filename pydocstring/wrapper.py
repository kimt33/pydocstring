import difflib
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
    if obj.__doc__ is None:
        obj.__doc__ = ''

    if style == 'numpy':
        docstring = Docstring(**parse_numpy(obj.__doc__, contains_quotes=False))
    elif style == 'code':
        docstring = obj.__doc__
    else:
        raise NotImplementedError('Only numpy and code (Docstring instance) style are supported at '
                                  'the moment.')
    # generate new docstring
    new_doc = docstring.make_numpy(width=width, indent_level=indent_level, tabsize=tabsize,
                                   is_raw=is_raw, include_quotes=False)
    # compare to original
    if style == 'numpy':
        # FIXME: move to a better location
        diff = list(difflib.context_diff(obj.__doc__.strip().split('\n'),
                                         new_doc.strip().split('\n'),
                                         fromfile='original-{0}'.format(obj),
                                         tofile='generated-{0}'.format(obj)))
        if len(diff) != 0:
            print('WARNING: generated numpy docstring is different from the original')
            print('\n'.join(diff))
    # overwrite
    obj.__doc__ = new_doc

    # store Docstring instance
    # because attributes of property cannot be set
    if not isinstance(obj, property):
        obj._docstring = docstring

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


@kwarg_wrapper
def docstring_class(obj, style='numpy', width=100, indent_level=0, tabsize=4,
                    is_raw=False):
    """Wrapper for inheriting docstrings from parents and methods.

    Parameters
    ----------
    obj : class
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
        If the `obj` is not a class.
        If the obj's __doc__ is neither str nor Docstring instance.
    NotImplementedError
        If `style` is not 'numpy'.

    Returns
    -------
    obj
        Wrapped object where the docstring is in the selected format and the corresponding Docstring
        instance is stored in `_docstring`.

    """
    if not inspect.isclass(obj):
        raise TypeError('This decorator can only decorate classes.')

    # create docstrings
    obj = docstring_recursive(obj, style=style, width=width, indent_level=indent_level,
                              tabsize=tabsize, is_raw=is_raw)

    # inherit from parents
    for name, member in extract_members(obj).items():
        # FIXME: need to check if multiple parents have conflicting docstrings
        for parent in obj.__bases__:
            try:
                parent_member = getattr(parent, name)
                # the following is placed here rather than an else block b/c if parent does not have
                # _docstring attribute, AtributeError is also raised
                if isinstance(member, property):
                    # yet another pain the ass caused by property
                    member_docstring = Docstring(**parse_numpy(member.__doc__,
                                                               contains_quotes=False))
                    parent_docstring = Docstring(**parse_numpy(parent_member.__doc__,
                                                               contains_quotes=False))
                else:
                    member_docstring = member._docstring
                    parent_docstring = parent_member._docstring
            except AttributeError as error:
                continue
            else:
                member_docstring.inherit(parent_docstring, to_end=False)
                if hasattr(member, '_docstring'):
                    member._docstring = member_docstring
                member.__doc__ = member_docstring.make_numpy(width=width,
                                                             indent_level=indent_level+1,
                                                             tabsize=tabsize,
                                                             is_raw=is_raw,
                                                             include_quotes=False)

    # inherit docstring its contents
    member_doc = Docstring()
    for name, member in extract_members(obj).items():
        # because we cannot change the attributes of a property, it needs to be parsed and then
        # put back together...
        if isinstance(member, property):
            doc = Docstring(**parse_numpy(member.__doc__, contains_quotes=False))
        else:
            doc = member._docstring

        # fill contents
        contents = {'name': name, 'signature': '', 'types': '', 'descs': []}
        if 'returns' in doc.info:
            contents['types'] = [i for entry in doc.info['returns'] for i in entry.types]
        if 'summary' in doc.info:
            contents['descs'] = doc.info['summary']

        # get section name
        #  methods
        if inspect.isfunction(member):
            try:
                is_abstract = name in obj.__abstractmethods__
            except AttributeError:
                section = 'methods'
            else:
                section = 'abstract methods' if is_abstract else 'methods'
            # FIXME: only python 3.5+ has inspect.signature, I think.
            if hasattr(inspect, 'signature'):
                contents['signature'] = str(inspect.signature(member))

        #  properties
        elif isinstance(member, property):
            try:
                is_abstract = name in obj.__abstractmethods__
            except AttributeError:
                section = 'properties'
            else:
                section = 'abstract properties' if is_abstract else 'properties'
        # CHECK: this is a little redundant b/c extract_members does not contain attributes
        elif hasattr(obj, name):
            section = 'attributes'

        member_doc.inherit(Docstring(**{section: contents}), to_end=True)
    obj._docstring.inherit(member_doc, to_end=False)

    for parent in obj.__bases__:
        if not hasattr(parent, '_docstring'):
            continue
        # FIXME: need to check if multiple parents have conflicting docstrings
        obj._docstring.inherit(parent._docstring, to_end=False)

    obj.__doc__ = obj._docstring.make_numpy(width=width, indent_level=indent_level,
                                            tabsize=tabsize, is_raw=is_raw, include_quotes=False)

    return obj
