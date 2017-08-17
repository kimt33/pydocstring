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
    make_numpy()
        Return corresponding numpy docstring

    Example
    -------
    For example, this docstring should be equivalent to

    info = {'Attributes': {'info': {'type': ['dict'],
                           'docs':['Dictionary of the headers to contents under header.']}}}
    info = {'Attributes': {'info': <ParamDocstring object>}}
    """
    pass


class ParamDocstring:
    """Class for storing docstring information on parameters.

    Attributes
    ----------
    name : str
        Name of the parameter.
    types : list of str
        Type of the parameters allowed.
    docs : list of str
        Documentations for the parameter.

    Methods
    -------
    __init__(name, type=None, docs=None)
        Initialize.
    parse_google(docstring)
        Return instance of Docstring that corresponds to given google docstring.
    parse_numpy(docstring)
        Return instance of Docstring that corresponds to given numpy docstring.
    """
    pass


class MethodDocstring:
    """Class for storing docstring information on methods.

    Attributes
    ----------
    name : str
        Name of the method.
    call_signature : str
        Call signature of the method.
    docs : list of str
        Documentations for the method.

    Methods
    -------
    __init__(name, call_signature, docs=None)
        Initialize.
    parse_google(docstring)
        Return instance of Docstring that corresponds to given google docstring.
    parse_numpy(docstring)
        Return instance of Docstring that corresponds to given numpy docstring.
    """
    pass
