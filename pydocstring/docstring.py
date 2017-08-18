import textwrap


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
    def __init__(self, **headers_contents):
        """Initializes.

        Parameters
        ----------
        headers_contents : dict from str to str/dict
            Section title and the contents of that section
            For 'extended', list/tuple of string needs to be provided (one for each paragraph).
            For 'parameters', list of dictionaries needed to be provided for constructing
            ParamDocstring.
            For 'methods', list of dictionaries needed to be provided for constructing
            MethodDocstring.
            For 'returns' and 'yields', list of dictionaries needed to be provided for constructing
            ParamDocstring or MethodDocstring.
        """
        headers_contents = {key.lower(): val for key, val in headers_contents.items()}
        # contents
        self.info = {}
        for key, val in headers_contents.items():
            if key == 'parameters':
                self.info[key] = [ParamDocstring(**param_dict) for param_dict in val]
            elif key == 'methods':
                self.info[key] = [MethodDocstring(**method_dict) for method_dict in val]
            elif key in ['returns', 'yields']:
                returns = []
                for info_dict in val:
                    try:
                        returns.append(ParamDocstring(**info_dict))
                    except KeyError:
                        returns.append(MethodDocstring(**info_dict))
                self.info[key] = returns
            elif key in ['raises']:
                self.info[key] = [RaiseDocstring(**raise_dict) for raise_dict in val]
            else:
                self.info[key] = val

            if key not in ['summary', 'extended', 'parameters', 'other parameters', 'attributes',
                           'methods', 'returns', 'yields', 'raises', 'see also', 'notes',
                           'references', 'examples']:
                print('WARNING: keyword, {0}, is not available in the list.'.format(key))


# TODO: turn each section into a class
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
    __init__(name, types=None, docs=None)
        Initialize.
    make_google()
        Return correspond google docstring
    make_numpy()
        Return corresponding numpy docstring
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
    make_google()
        Return correspond google docstring
    make_numpy()
        Return corresponding numpy docstring
    """
    pass


class RaiseDocstring:
    """Class for storing docstring information on raises.

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
    make_google()
        Return correspond google docstring
    make_numpy()
        Return corresponding numpy docstring
    """
    pass
