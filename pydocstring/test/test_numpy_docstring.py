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
        docstring = ('summary\n\nblock1\n\nblock2\n\n{0}\n{1}\na\n    description1.\n'
                     '    description2.'.format(header.title(), '-'*len(header)))
        assert parse_numpy(docstring) == {'summary': 'summary',
                                          'extended': ['block1', 'block2'],
                                          header: [{'name': 'a',
                                                    'descs': ['description1.', 'description2.']}]}
        # name + types + multiple descriptions
        docstring = ('summary\n\nblock1\n\nblock2\n\n{0}\n{1}\na : str\n    description1.\n'
                     '    description2.'.format(header.title(), '-'*len(header)))
        assert parse_numpy(docstring) == {'summary': 'summary',
                                          'extended': ['block1', 'block2'],
                                          header: [{'name': 'a',
                                                    'types': ['str'],
                                                    'descs': ['description1.', 'description2.']}]}
        # name + signature + multiple descriptions
        docstring = ('summary\n\nblock1\n\nblock2\n\n{0}\n{1}\na(x, y)\n    description1.\n'
                     '    description2.'.format(header.title(), '-'*len(header)))
        assert parse_numpy(docstring) == {'summary': 'summary',
                                          'extended': ['block1', 'block2'],
                                          header: [{'name': 'a',
                                                    'signature': '(x, y)',
                                                    'descs': ['description1.', 'description2.']}]}
        # name + types + signature + multiple descriptions
        docstring = ('summary\n\nblock1\n\nblock2\n\n{0}\n{1}\na(x, y): str\n    description1.\n'
                     '    description2.'.format(header.title(), '-'*len(header)))
        assert parse_numpy(docstring) == {'summary': 'summary',
                                          'extended': ['block1', 'block2'],
                                          header: [{'name': 'a',
                                                    'types': ['str'],
                                                    'signature': '(x, y)',
                                                    'descs': ['description1.', 'description2.']}]}
        # name + types + signature + multiple descriptions - extended summary
        docstring = ('summary\n\n{0}\n{1}\na(x, y): str\n    description1.\n'
                     '    description2.'.format(header.title(), '-'*len(header)))
        assert parse_numpy(docstring) == {'summary': 'summary',
                                          header: [{'name': 'a',
                                                    'types': ['str'],
                                                    'signature': '(x, y)',
                                                    'descs': ['description1.', 'description2.']}]}

    # contains quotes
    docstring = ('"""summary"""')
    assert parse_numpy(docstring, contains_quotes=True) == {'summary': 'summary'}
    docstring = ('r"""sum\n\nmary"""')
    assert parse_numpy(docstring, contains_quotes=True) == {'summary': r'sum\n\nmary'}

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
