import pydocstring.utils


# FIXME: maybe use attributes to store header/section contents instead of a dictionary?
# FIXME: add tests
# TODO: math equations is a bit of a headache, especially because of the backslashes
class Docstring:
    """Class for storing docstring information.

    Following headers are used by this class:

    * 'summary' - first line of the docstring
    * 'extended' - blocks of extended description concerning the functionality of the code
    * 'parameters' - parameters of a method
    * 'other parameters' - parameters that are not commonly used
    * 'returns' - returned value of a method
    * 'yields' - generated value of a generator
    * 'raises' - errors raised
    * 'see also' - other related code
    * 'notes' - blocks of other information about the code (e.g. implementation details)
    * 'references' - references used
    * 'examples' - examples of code usage
    * 'attributes' - attributes of a class
    * 'methods' - methods of a class/module

    Attributes
    ----------
    info : dict
        Dictionary of the headers to contents under header.

    Methods
    -------
    __init__(**headers_contents)
        Initialize.
    parse_google(docstring)
        Return instance of Docstring that corresponds to given google docstring.
    parse_numpy(docstring)
        Return instance of Docstring that corresponds to given numpy docstring.
    parse_instance(instance)
        Return instance of Docstring that corresponds to provided instance.
    make_google()
        Return corresponding google docstring
    make_numpy(self, width=100, indent_level=0, tabsize=4)
        Return corresponding numpy docstring

    Example
    -------
    For example, this docstring should be equivalent to

    info = {'Attributes': {'info': {'type': ['dict'],
                                    'descs':['Dictionary of the headers to contents under header.']}
                           }}
    info = {'Attributes': {'info': <TabbedInfo object>}}
    """
    # FIXME: probably hardcodes the numpy docstring style
    # FIXME: multi-word headers are troublesome
    def __init__(self, **headers_contents):
        """Initializes.

        For 'summary', 'parameters', 'other parameters', 'attributes', 'methods', 'returns',
        'yields'. 'raises', and 'see also' keywords, the contents are fed into the TabbedInfo
        initializer as keyword arguments.

        Parameters
        ----------
        headers_contents : dict
            Section title and the contents of that section
            'summary' : str
            'extended' : {str, list of str}
            'parameters' : {None, TabbedInfo, dict}
            'other parameters' : {None, TabbedInfo, dict}
            'attributes' : {None, TabbedInfo, dict}
            'methods' : {None, TabbedInfo, dict}
            'returns' : {None, TabbedInfo, dict}
            'yields' : {None, TabbedInfo, dict}
            'raises' : {None, TabbedInfo, dict}
            'see also' : {None, TabbedInfo, dict}
            'notes' : {str, list of str}
            'references' : {str, list of str}
            'examples' : {str, list of str}

        Raises
        ------
        TypeError
            If sections 'Parameters', 'Other Parameters', 'Attributes', 'Methods', 'Returns',
            'Yields', 'Raises', and 'See Also' have items that are not instances of TabbedInfo or
            parameters to the initializer of these classes.
            If the summary or other sections (i.e. not listed above) has contents that are not
            string.
        """
        self.info = {}

        headers_contents = {key.lower(): val for key, val in headers_contents.items()}
        for key, contents in headers_contents.items():
            if key in ['parameters', 'other parameters', 'attributes', 'methods', 'returns',
                       'yields', 'raises', 'see also', 'properties', 'abstract properties',
                       'abstract methods']:
                data = []
                if not isinstance(contents, (list, tuple)):
                    contents = [contents]

                for item in contents:
                    if isinstance(item, TabbedInfo):
                        data.append(item)
                        continue

                    try:
                        data.append(TabbedInfo(**item))
                    except TypeError as error:
                        # NOTE: this breaks python2 compatibility
                        raise TypeError(
                            'Items of section, {0}, must be an instance of `TabbedInfo` or be the '
                            'parameters to the initializer of these clases.'.format(key)
                        ) from error
                self.info[key] = data
            elif key in ['extended', 'notes', 'references', 'examples']:
                if isinstance(contents, str):
                    self.info[key] = [contents]
                else:
                    self.info[key] = list(contents)
            elif isinstance(contents, str):
                self.info[key] = contents
            else:
                raise TypeError('The contents of the section, {0}, must be a string'.format(key))

            if key not in ['summary', 'extended', 'parameters', 'other parameters', 'attributes',
                           'methods', 'returns', 'yields', 'raises', 'see also', 'notes',
                           'references', 'examples']:
                print('WARNING: keyword, {0}, is not compatible with the numpy write.'.format(key))

    # FIXME: all keywords that are not in numpy's doc sections will not be added
    def make_numpy(self, width=100, indent_level=0, tabsize=4, is_raw=False):
        """Returns the numpy docstring that corresponds to the Docstring instance.

        Parameters
        ----------
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
        """
        wrap_kwargs = {'width': width, 'indent_level': indent_level,
                       'tabsize': tabsize}

        output = pydocstring.utils.wrap('{0}{1}'.format('r' if is_raw else '', '"""'),
                                        **wrap_kwargs)
        # summary
        if 'summary' not in self.info:
            pass
            # NOTE: is this too harsh?
            # raise NotImplementedError('Summary needs to be provided to construct the numpy'
            #                           ' documentation.')
        elif len(self.info['summary']) < (width
                                          - (6 if len(self.info) == 1 else 3)
                                          - (1 if is_raw else 0)):
            output += self.info['summary']
        elif len(self.info['summary']) < width:
            output += '\n{0}'.format(pydocstring.utils.wrap(self.info['summary'], **wrap_kwargs))
        else:
            print('WARNING: summary is too long for the given indent level and line length.')
            output += self.info['summary']

        # extended
        # FIXME: textwrap is not terribly reliable
        # FIXME: multiline string will contain all the tabs/spaces. these need to be removed
        if 'extended' in self.info:
            for paragraph in self.info['extended']:
                output += '\n\n{0}'.format(pydocstring.utils.wrap(paragraph, **wrap_kwargs))

        # set the order of documentation construction
        sections = ['parameters', 'other parameters', 'attributes', 'properties',
                    'abstract properties', 'methods', 'abstract methods', 'returns', 'yields',
                    'raises', 'see also', 'notes', 'references', 'examples']
        for section in sections:
            if section not in self.info:
                continue
            # create header
            output += '\n\n{0}\n{1}'.format(pydocstring.utils.wrap(section.title(), **wrap_kwargs),
                                            pydocstring.utils.wrap('-'*len(section), **wrap_kwargs))

            for i, entry in enumerate(self.info[section]):
                if section == 'references':
                    output += '\n.. '
                    # add three spaces for subsequent lines to account for '.. '
                    output += pydocstring.utils.wrap('[{0}] {1}'.format(i+1, entry),
                                                     added_indent='   ', remove_initial_indent=True,
                                                     **wrap_kwargs)
                elif isinstance(entry, str):
                    # number of newlines before the block
                    num_spaces = 1 if i > 0 else 0
                    output += '{0}\n{1}'.format('\n'*num_spaces,
                                                pydocstring.utils.wrap(entry, **wrap_kwargs))
                else:
                    output += '\n{0}'.format(entry.make_numpy(width=width,
                                                              indent_level=indent_level,
                                                              tabsize=tabsize))

        output += '\n{0}'.format(pydocstring.utils.wrap('"""', **wrap_kwargs))
        return output


# FIXME: rename
class TabbedInfo:
    """Class for storing docstring information where subsequent lines are tabbed.

    If the information is a method, then all of `name`, `signature`, and `descs` can be
    given. The `types` can also be given to show the types of the returned value. However, note that
    NumPy docstring format does not support this documentation format.
    If the information is a parameter, then `name`, `type` and `descs` can be given. The `types`
    would correspond to the allowed types of the parameter.
    If the information is a raised error, then `name` and `descs` can be given.

    Attributes
    ----------
    name : str
        Name of the information.
    signature : {str, None}
        Signature of the information.
        Used for methods.
    types : {str, list of str, None}
        Type of the information.
        Used to describe types of a parameter and of the value returned by a method.
    descs : {str, list of str, None}
        Description of the information.

    Methods
    -------
    __init__(name, descs=None)
        Initialize.
    make_google()
        Return correspond google docstring
    make_numpy()
        Return corresponding numpy docstring
    """
    def __init__(self, name, signature='', types='', descs=''):
        """Initialize.

        Parameters
        ----------
        name : str
            Name of the information.
        signature : {str, ''}
            Signature of the information.
            Used for methods.
            Default is no signature.
        types : {str, list of str, ''}
            Type of the information.
            Used for parameters and methods (value returned).
            Default is no types.
        descs : {str, list of str, ''}
            Descriptions of the information.
            Default is no description.

        Raises
        ------
        TypeError
            If the `name` is not a string.
            If the `signature` is not a string.
            If the `types` is not a string or a list/tuple of string.
            If the `descs` is not a string or a list/tuple of string.
        """
        # name
        if not isinstance(name, str):
            raise TypeError('`name` must be a string.')
        self.name = name

        # signature
        if not isinstance(signature, str):
            raise TypeError('`signature` must be a string.')
        elif signature != '':
            signature = signature.strip()
            if signature[0] != '(' or signature[-1] != ')':
                signature = '({0})'.format(signature)
        self.signature = signature

        # types
        if isinstance(types, str):
            # remove empty string
            self.types = [i for i in [types] if i != '']
        elif isinstance(types, (list, tuple)) and all(isinstance(i, str) for i in types):
            self.types = list(types)
        else:
            raise TypeError('`types` must be a string or a list/tuple of strings.')

        # descriptions
        if isinstance(descs, str):
            # remove empty string
            self.descs = [i for i in [descs] if i != '']
        elif isinstance(descs, (list, tuple)):
            self.descs = list(descs)
        else:
            raise TypeError('`descs` must be a string or a list/tuple of strings')

    def make_numpy(self, width=100, indent_level=0, tabsize=4):
        """Returns the numpy docstring that corresponds to the TabbedInfo instance.

        Parameters
        ----------
        width : int
            Maximum number of characters allowed in each width
        indent_level : int
            Number of indents (tabs) that are needed for the docstring
        tabsize : int
            Number of spaces that corresponds to a tab
        """
        wrap_kwargs = {'width': width, 'expand_tabs': True, 'tabsize': tabsize,
                       'replace_whitespace': False, 'drop_whitespace': True,
                       'break_long_words': False}

        # first line
        # NOTE: add subsequent indent just in case signature and types are long enough to wrap
        if self.signature != '' and len(self.types) > 0:
            raise NotImplementedError('NumPy documentation format does not support methods with '
                                      'the type of the returned values.')

        if len(self.types) == 0:
            signature = self.signature if self.signature != '' else ''
            output = pydocstring.utils.wrap('{0}{1}'.format(self.name, signature),
                                            indent_level=indent_level,
                                            added_indent=('', ' ' * (len(self.name) + 1)),
                                            **wrap_kwargs)
        elif len(self.types) == 1:
            output = pydocstring.utils.wrap('{0} : {1}'.format(self.name, self.types[0]),
                                            indent_level=indent_level,
                                            added_indent=('', ' ' * (len(self.name) + 3)),
                                            **wrap_kwargs)
        elif len(self.types) > 1:
            output = pydocstring.utils.wrap('{0} : {1}{2}{3}'.format(self.name, '{',
                                                                     ', '.join(self.types), '}'),
                                            indent_level=indent_level,
                                            added_indent=('', ' ' * (len(self.name) + 4)),
                                            **wrap_kwargs)
        # subsequent lines
        for description in self.descs:
            output += '\n{0}'.format(pydocstring.utils.wrap(description,
                                                            indent_level=indent_level + 1,
                                                            **wrap_kwargs))

        return output
