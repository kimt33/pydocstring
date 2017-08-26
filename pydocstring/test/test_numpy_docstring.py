from nose.tools import assert_raises
from pydocstring.numpy_docstring import parse_numpy


def test_parse_numpy():
    """Tests pydocstring.numpy_docstring.parse_numpy."""
    # summary
    docstring = 'summary'
    assert parse_numpy(docstring) == {'summary': 'summary'}
    docstring = 'summary\n'
    assert parse_numpy(docstring) == {'summary': 'summary'}
    docstring = '\nsummary\n'
    assert parse_numpy(docstring) == {'summary': 'summary'}
    # FIXME: this should raise an error
    docstring = '\n\nsummary\n'
    assert parse_numpy(docstring) == {'summary': '', 'extended': ['summary']}

    # extended
    docstring = 'summary\n\nblock1\n\nblock2'
    assert parse_numpy(docstring) == {'summary': 'summary', 'extended': ['block1', 'block2']}
    docstring = '\nsummary\n\nblock1\n\nblock2'
    assert parse_numpy(docstring) == {'summary': 'summary', 'extended': ['block1', 'block2']}
    # FIXME: bug or feature?
    docstring = '\n\nsummary\n\nblock1\n\nblock2'
    assert parse_numpy(docstring) == {'summary': '', 'extended': ['summary', 'block1', 'block2']}
    # extended + headers
    docstring = 'summary\n\nblock1\n\nblock2\n\nheader\n------\nstuff'
    assert parse_numpy(docstring) == {'summary': 'summary',
                                      'extended': ['block1', 'block2'],
                                      'header': ['stuff']}

    # headers
    docstring = 'summary\n\nblock1\n\nblock2\n\nheader1\n--\n\n'
    assert_raises(ValueError, parse_numpy, docstring)

    for header in ['parameters', 'attributes', 'methods', 'returns', 'yields', 'raises',
                   'other parameters', 'see also']:
        # name + multiple descriptions
        docstring = ('summary\n\nblock1\n\nblock2\n\n{0}\n{1}\nabc\n    description1.\n'
                     '    description2.'.format(header.title(), '-'*len(header)))
        assert parse_numpy(docstring) == {'summary': 'summary',
                                          'extended': ['block1', 'block2'],
                                          header: [{'name': 'abc',
                                                    'descs': ['description1.', 'description2.']}]}
        # name + types + multiple descriptions
        docstring = ('summary\n\nblock1\n\nblock2\n\n{0}\n{1}\nabc : str\n    description1.\n'
                     '    description2.'.format(header.title(), '-'*len(header)))
        assert parse_numpy(docstring) == {'summary': 'summary',
                                          'extended': ['block1', 'block2'],
                                          header: [{'name': 'abc',
                                                    'types': ['str'],
                                                    'descs': ['description1.', 'description2.']}]}
        # name + signature + multiple descriptions
        docstring = ('summary\n\nblock1\n\nblock2\n\n{0}\n{1}\nabc(x, y)\n    description1.\n'
                     '    description2.'.format(header.title(), '-'*len(header)))
        assert parse_numpy(docstring) == {'summary': 'summary',
                                          'extended': ['block1', 'block2'],
                                          header: [{'name': 'abc',
                                                    'signature': '(x, y)',
                                                    'descs': ['description1.', 'description2.']}]}
        # name + types + signature + multiple descriptions
        docstring = ('summary\n\nblock1\n\nblock2\n\n{0}\n{1}\nabc(x, y): str\n    description1.\n'
                     '    description2.'.format(header.title(), '-'*len(header)))
        assert parse_numpy(docstring) == {'summary': 'summary',
                                          'extended': ['block1', 'block2'],
                                          header: [{'name': 'abc',
                                                    'types': ['str'],
                                                    'signature': '(x, y)',
                                                    'descs': ['description1.', 'description2.']}]}
        # name + types + signature + multiple descriptions - extended summary
        docstring = ('summary\n\n{0}\n{1}\nabc(x, y): str\n    description1.\n'
                     '    description2.'.format(header.title(), '-'*len(header)))
        assert parse_numpy(docstring) == {'summary': 'summary',
                                          header: [{'name': 'abc',
                                                    'types': ['str'],
                                                    'signature': '(x, y)',
                                                    'descs': ['description1.', 'description2.']}]}
        # name + types
        docstring = ('summary\n\n{0}\n{1}\nabc: str\ndef: int'.format(header.title(),
                                                                      '-'*len(header)))
        assert parse_numpy(docstring) == {'summary': 'summary',
                                          header: [{'name': 'abc',
                                                    'types': ['str']},
                                                   {'name': 'def',
                                                    'types': ['int']}]}


def test_parse_numpy_raw():
    """Test pydocstring.numpy_docstring.parse_numpy with raw strings."""
    docstring = '"""summary\n\nextended"""'
    assert parse_numpy(docstring, contains_quotes=True) == {'summary': 'summary',
                                                            'extended': ['extended']}
    docstring = 'r"""summary\n\nextended"""'
    assert_raises(NotImplementedError, parse_numpy, docstring, contains_quotes=True)


def test_parse_numpy_self():
    """Test pydocstring.numpy_docstring.parse_numpy using itself as an example."""
    docstring = parse_numpy.__doc__
    assert (parse_numpy(docstring, contains_quotes=False)['summary'] ==
            'Extract numpy docstring as a dictionary.')
    assert (parse_numpy(docstring, contains_quotes=False)['extended'] ==
            ['Multiple descriptions of the indented information (e.g. parameters, '
             'attributes, methods, returns, yields, raises, see also) are '
             'distinguished from one another with a period. If the period is not '
             'present, then the description is assumed to be a multiline '
             'description.'])
    assert (parse_numpy(docstring, contains_quotes=False)['parameters'] ==
            [{'name': 'docstring',
              'types': ['str'],
              'descs': ['Numpy docstring.']},
             {'name': 'contains_quotes',
              'types': ['bool'],
              'descs': ['True if docstring contains """ or \'\'\'.']}])
    assert (parse_numpy(docstring, contains_quotes=False)['returns'] ==
            [{'name': 'output',
              'types': ['dict'],
              'descs': ['Contents of the docstring separated into different section.',
                        'If the section is summary, then the value is string.',
                        'If the section is extended, notes, references, or examples, '
                        'then the value is list of strings.',
                        'If the section is parameters, other parameters, attributes, '
                        'methods, returns, yields, raises, or see also, then the value '
                        'is a dictionary with keys \'name\', \'signature\', \'types\', '
                        'or \'docs\', with corresonding values string, string, list of '
                        'strings, and list of strings, respectively.',
                        'Otherwise, the values is a list of strings.']}])
    assert (parse_numpy(docstring, contains_quotes=False)['raises'] ==
            [{'name': 'ValueError',
              'descs': ['If summary is not in the first or second line.',
                        'If summary is now followed with a blank line.',
                        'If number of \'-\' does not match the number of characters in '
                        'the header.',
                        'If given entry of the tabbed information (parameters, '
                        'attributes, methods, returns, yields, raises, see also) '
                        'had an unexpected pattern.']},
             {'name': 'NotImplementedError',
              'descs': ['If quotes corresponds to a raw string, i.e. r""".']}])


def test_parse_numpy_equations():
    """Test pydocstring.numpy_docstring.parse_numpy with equations."""
    # contains equations
    docstring = ('summary\n\n.. math::\n\n    \\frac{1}{2}')
    assert parse_numpy(docstring) == {'summary': 'summary',
                                      'extended': ['.. math::', '    \\frac{1}{2}']}
    docstring = ('summary\n\nParameters\n----------\na : float\n    .. math::\n\n    '
                 '    \\frac{1}{2}')
    # single line equation
    assert parse_numpy(docstring) == {'summary': 'summary',
                                      'parameters': [{'name': 'a',
                                                      'types': ['float'],
                                                      'descs': ['.. math::\n\n    \\frac{1}{2}\n']}]
                                      }
    # multi line equation
    docstring = ('summary\n\nParameters\n----------\na : float\n    .. math::\n\n'
                 '        \\frac{1}{2}\\\\\n        \\frac{1}{3}')
    assert parse_numpy(docstring) == {'summary': 'summary',
                                      'parameters': [{'name': 'a',
                                                      'types': ['float'],
                                                      'descs': ['.. math::\n\n    \\frac{1}{2}\\\\'
                                                                '\n    \\frac{1}{3}\n']}]
                                      }
    # multiple equations
    docstring = ('summary\n\nParameters\n----------\na : float\n    .. math::\n\n'
                 '        \\frac{1}{2}\n    ..math::\n        \\frac{1}{3}')
    assert parse_numpy(docstring) == {'summary': 'summary',
                                      'parameters': [{'name': 'a',
                                                      'types': ['float'],
                                                      'descs': ['.. math::\n\n    \\frac{1}{2}\n',
                                                                '..math::\n    \\frac{1}{3}\n']}]
                                      }
    # multiple equations and other descriptions
    docstring = ('summary\n\nParameters\n----------\na : float\n    Some float.\n    .. math::\n\n'
                 '        \\frac{1}{2}\n\n    Yes.\n    ..math::\n        \\frac{1}{3}\n'
                 '    This is the float.')
    assert parse_numpy(docstring) == {'summary': 'summary',
                                      'parameters': [{'name': 'a',
                                                      'types': ['float'],
                                                      'descs': ['Some float.',
                                                                '.. math::\n\n    \\frac{1}{2}\n',
                                                                'Yes.',
                                                                '..math::\n    \\frac{1}{3}\n',
                                                                'This is the float.']}]
                                      }
