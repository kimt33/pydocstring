import textwrap


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
    make_numpy(self, line_length=100, indent_level=0, tab_width=4)
        Return corresponding numpy docstring

    Example
    -------
    For example, this docstring should be equivalent to

    info = {'Attributes': {'info': {'type': ['dict'],
                                    'descs':['Dictionary of the headers to contents under header.']}
                           }}
    info = {'Attributes': {'info': <ParamInfo object>}}
    """
    # FIXME: probably hardcodes the numpy docstring style
    # FIXME: multi-word headers are troublesome
    def __init__(self, **headers_contents):
        """Initializes.

        For 'summary', 'parameters', 'other parameters', 'attributes', 'methods', 'returns',
        'yields'. 'raises', and 'see also' keywords, the contents are fed into the ParamInfo,
        MethodInfo or TabbedInfo initializer as keyword arguments.

        Parameters
        ----------
        headers_contents : dict
            Section title and the contents of that section
            'summary' : str
            'extended' : {str, list of str}
            'parameters' : {None, ParamInfo, MethodInfo, TabbedInfo, dict}
            'other parameters' : {None, ParamInfo, MethodInfo, TabbedInfo, dict}
            'attributes' : {None, ParamInfo, MethodInfo, TabbedInfo, dict}
            'methods' : {None, ParamInfo, MethodInfo, TabbedInfo, dict}
            'returns' : {None, ParamInfo, MethodInfo, TabbedInfo, dict}
            'yields' : {None, ParamInfo, MethodInfo, TabbedInfo, dict}
            'raises' : {None, ParamInfo, MethodInfo, TabbedInfo, dict}
            'see also' : {None, ParamInfo, MethodInfo, TabbedInfo, dict}
            'notes' : {str, list of str}
            'references' : {str, list of str}
            'examples' : {str, list of str}

        Raises
        ------
        TypeError
            If sections 'Parameters', 'Other Parameters', 'Attributes', 'Methods', 'Returns',
            'Yields', 'Raises', and 'See Also' have items that are not instances of ParamInfo,
            MethodInfo, TabbedInfo or parameters to the initializer of these classes.
            If the summary or other sections (i.e. not listed above) has contents that are not
            string.
        """
        self.info = {}

        headers_contents = {key.lower(): val for key, val in headers_contents.items()}
        for key, contents in headers_contents.items():
            if key in ['parameters', 'other parameters', 'attributes', 'methods', 'returns',
                       'yields', 'raises', 'see also']:
                data = []
                if not isinstance(contents, (list, tuple)):
                    contents = [contents]

                for item in contents:
                    if isinstance(item, (ParamInfo, MethodInfo, TabbedInfo)):
                        data.append(item)
                        continue

                    try:
                        data.append(ParamInfo(**item))
                        continue
                    except TypeError:
                        pass

                    try:
                        data.append(MethodInfo(**item))
                        continue
                    except TypeError:
                        pass

                    try:
                        data.append(TabbedInfo(**item))
                        continue
                    except TypeError:
                        pass

                    raise TypeError(
                        'Items of section, {0}, must be an instance of `ParamInfo` or '
                        '`MethodInfo`, `TabbedInfo` or be the parameters to the '
                        'initializer of these clases.'.format(key)
                    )
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
    def make_numpy(self, line_length=100, indent_level=0, tab_width=4, is_raw=False):
        """Returns the numpy docstring that corresponds to the Docstring instance.

        Parameters
        ----------
        line_length : int
            Maximum number of characters allowed in each width
        indent_level : int
            Number of indents (tabs) that are needed for the docstring
        tab_width : int
            Number of spaces that corresponds to a tab
        is_raw : bool
            True if the generated numpy documentation string is a raw string. Docstring should be
            raw when backslash is used (e.g. math equations).
            Default is False.
        """
        avail_width = line_length - tab_width * indent_level
        tab = '{0}'.format(tab_width * indent_level * ' ')
        wrapper = textwrap.TextWrapper(width=avail_width, expand_tabs=True, tabsize=tab_width,
                                       replace_whitespace=False, drop_whitespace=True,
                                       initial_indent=tab, subsequent_indent=tab,
                                       break_long_words=False)

        output = wrapper.fill('{0}{1}'.format('r' if is_raw else '', '"""'))
        # summary
        # FIXME: what if summary is not given?
        if len(self.info['summary']) < (avail_width
                                        - (6 if len(self.info) == 1 else 3)
                                        - (1 if is_raw else 0)):
            output += '{0}'.format(self.info['summary'])
        elif len(self.info['summary']) < avail_width:
            output += '\n{0}'.format(wrapper.fill(self.info['summary']))
        else:
            print('WARNING: summary is too long for the given indent level and line length.')
            output += '{0}'.format(self.info['summary'])

        # extended
        # FIXME: textwrap is not terribly reliable
        # FIXME: multiline string will contain all the tabs/spaces. these need to be removed
        if 'extended' in self.info:
            for paragraph in self.info['extended']:
                output += '\n\n{0}'.format(wrapper.fill(paragraph))

        # Sections that contains list/tuple of ParamInfo, MethodInfo or TabbedInfo
        # make a list just in case dictionaries stop being ordered
        sections = ['parameters', 'other parameters', 'attributes', 'methods', 'returns', 'yields',
                    'raises', 'see also']
        headers = {'parameters': 'Parameters',
                   'other parameters': 'Other Parameters',
                   'attributes': 'Attributes',
                   'methods': 'Methods',
                   'returns': 'Returns',
                   'yields': 'Yields',
                   'raises': 'Raises',
                   'see also': 'See Also'}
        for section in sections:
            if section not in self.info:
                continue
            output += '\n\n{0}\n{1}'.format(wrapper.fill(headers[section]),
                                            wrapper.fill('-'*len(headers[section])))
            for data in self.info[section]:
                output += '\n{0}'.format(data.make_numpy(line_length=line_length,
                                                         indent_level=indent_level,
                                                         tab_width=tab_width))

        # Sections that contains list of strings
        sections = ['notes', 'references', 'examples']
        headers = {'notes': 'Notes',
                   'references': 'References',
                   'examples': 'Examples'}
        for section in sections:
            if section not in self.info:
                continue
            output += '\n\n{0}\n{1}'.format(wrapper.fill(headers[section]),
                                            wrapper.fill('-'*len(headers[section])))
            for i, paragraph in enumerate(self.info[section]):
                if section == 'references':
                    wrapper.subsequent_indent = tab + 3*' '
                    wrapper.width -= 3
                    output += '\n.. {0}'.format(wrapper.fill('[{0}] {1}'.format(i+1, paragraph)))
                    wrapper.subsequent_indent = tab
                    wrapper.width += 3
                else:
                    output += '{0}\n{1}'.format('\n' if i > 0 else '', wrapper.fill(paragraph))

        output += '\n{0}'.format(wrapper.fill('"""'))
        return output


class TabbedInfo:
    """Class for storing docstring information where subsequent lines are tabbed.

    For example, '''something\n    description''' can be described by this class.

    Attributes
    ----------
    name : str
        Name of the information.
    descs : list of str
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
    def __init__(self, name, descs=None):
        """Initialize ParamInfo.

        Parameters
        ----------
        name : str
            Name of the method.
        descs : tuple/list of str
            Each point of documentation of the method.
        """
        self.name = name
        if descs is None:
            self.descs = []
        elif isinstance(descs, str):
            self.descs = [descs]
        elif isinstance(descs, (list, tuple)):
            self.descs = list(descs)
        else:
            raise TypeError('descs must be a string or a list/tuple of strings')

    def make_numpy(self, line_length=100, indent_level=0, tab_width=4):
        """Returns the numpy docstring that corresponds to the TabbedInfo instance.

        Parameters
        ----------
        line_length : int
            Maximum number of characters allowed in each width
        indent_level : int
            Number of indents (tabs) that are needed for the docstring
        tab_width : int
            Number of spaces that corresponds to a tab
        """
        avail_width = line_length - tab_width * indent_level
        tab = '{0}'.format(tab_width * indent_level * ' ')
        wrapper_kwargs = {'width': avail_width, 'expand_tabs': True, 'tabsize': tab_width,
                          'replace_whitespace': False, 'drop_whitespace': True,
                          'break_long_words': False}

        output = ''
        # first line
        # NOTE: add subsequent indent just in case the types are long enough to wrap
        output += textwrap.fill('{0}'.format(self.name),
                                initial_indent=tab, subsequent_indent=tab, **wrapper_kwargs)
        # subsequent lines
        for description in self.descs:
            output += '\n{0}'.format(textwrap.fill(description,
                                                   initial_indent=tab + tab_width*' ',
                                                   subsequent_indent=tab + tab_width*' ',
                                                   **wrapper_kwargs))

        return output


class ParamInfo(TabbedInfo):
    """Class for storing docstring information on parameters.

    Attributes
    ----------
    name : str
        Name of the parameter.
    types : list of str
        Type of the parameters allowed.
    descs : list of str
        Documentations for the parameter.

    Methods
    -------
    __init__(name, types=None, descs=None)
        Initialize.
    make_google()
        Return correspond google docstring
    make_numpy(self, line_length=100, indent_level=0, tab_width=4)
        Return corresponding numpy docstring
    """
    def __init__(self, name, types, descs=None):
        """Initialize ParamInfo.

        Parameters
        ----------
        name : str
            Name of the parameter.
        types : {tuple/list of str, str}
            Allowed types of the parameter
        descs : tuple/list of str
            Each point of documentation of the parameter.

        Raises
        ------
        TypeError
            If types of the parameter is not a string or a list/tuple of strings
        """
        super().__init__(name, descs)
        if isinstance(types, str):
            self.types = [types]
        elif isinstance(types, (list, tuple)) and all(isinstance(i, str) for i in types):
            self.types = list(types)
        else:
            raise TypeError('Types allowed by the parameter must be given as a string.')

    # FIXME: maybe use super().make_numpy somehow?
    def make_numpy(self, line_length=100, indent_level=0, tab_width=4):
        """Returns the numpy docstring that corresponds to the ParamInfo instance.

        Parameters
        ----------
        line_length : int
            Maximum number of characters allowed in each width
        indent_level : int
            Number of indents (tabs) that are needed for the docstring
        tab_width : int
            Number of spaces that corresponds to a tab
        """
        avail_width = line_length - tab_width * indent_level
        tab = '{0}'.format(tab_width * indent_level * ' ')
        wrapper_kwargs = {'width': avail_width, 'expand_tabs': True, 'tabsize': tab_width,
                          'replace_whitespace': False, 'drop_whitespace': True,
                          'break_long_words': False}

        output = ''
        # first line
        # NOTE: add subsequent indent just in case the types are long enough to wrap
        if len(self.types) == 1:
            output += textwrap.fill('{0} : {1}'.format(self.name, self.types[0]),
                                    initial_indent=tab,
                                    subsequent_indent=tab + ' '*(len(self.name)+3),
                                    **wrapper_kwargs)
        else:
            output += textwrap.fill('{0} : {1}{2}{3}'.format(self.name, '{', ', '.join(self.types),
                                                             '}'),
                                    initial_indent=tab,
                                    subsequent_indent=tab + ' '*(len(self.name)+4),
                                    **wrapper_kwargs)
        # subsequent lines
        for description in self.descs:
            output += '\n{0}'.format(textwrap.fill(description,
                                                   initial_indent=tab + tab_width*' ',
                                                   subsequent_indent=tab + tab_width*' ',
                                                   **wrapper_kwargs))

        return output


class MethodInfo(TabbedInfo):
    """Class for storing docstring information on methods.

    Attributes
    ----------
    name : str
        Name of the method.
    signature : str
        Signature of the method.
    descs : list of str
        Documentations for the method.

    Methods
    -------
    __init__(name, signature, descs=None)
        Initialize.
    make_google()
        Return correspond google docstring
    make_numpy(self, line_length=100, indent_level=0, tab_width=4)
        Return corresponding numpy docstring
    """
    def __init__(self, name, signature, descs=None):
        """Initialize ParamInfo.

        Parameters
        ----------
        name : str
            Name of the method.
        signature : str
            Signature of the method.
        descs : tuple/list of str
            Each point of documentation of the method.

        Raises
        ------
        TypeError
            If signatur is not a string.
        """
        super().__init__(name, descs)
        # FIXME: this can be broken with the right parenthesis structure
        if not isinstance(signature, str):
            raise TypeError('signature must be a string.')
        signature = signature.strip()
        if signature[0] != '(' or signature[-1] != ')':
            signature = '({0})'.format(signature)
        self.signature = signature

    # FIXME: maybe use super().make_numpy somehow?
    def make_numpy(self, line_length=100, indent_level=0, tab_width=4):
        """Returns the numpy docstring that corresponds to the MethodInfo instance.

        Parameters
        ----------
        line_length : int
            Maximum number of characters allowed in each width
        indent_level : int
            Number of indents (tabs) that are needed for the docstring
        tab_width : int
            Number of spaces that corresponds to a tab
        """
        avail_width = line_length - tab_width * indent_level
        tab = '{0}'.format(tab_width * indent_level * ' ')
        wrapper_kwargs = {'width': avail_width, 'expand_tabs': True, 'tabsize': tab_width,
                          'replace_whitespace': False, 'drop_whitespace': True,
                          'break_long_words': False}

        output = ''
        # first line
        # NOTE: add subsequent indent just in case the types are long enough to wrap
        output += textwrap.fill('{0}{1}'.format(self.name, self.signature),
                                initial_indent=tab, subsequent_indent=tab + ' '*(len(self.name)+1),
                                **wrapper_kwargs)
        # subsequent lines
        for description in self.descs:
            output += '\n{0}'.format(textwrap.fill(description,
                                                   initial_indent=tab + tab_width*' ',
                                                   subsequent_indent=tab + tab_width*' ',
                                                   **wrapper_kwargs))

        return output
