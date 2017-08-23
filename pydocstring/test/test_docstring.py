from nose.tools import assert_raises
from pydocstring import docstring


def test_docstring_init():
    """Tests Docstring.__init__."""
    # Summary
    docstr = docstring.Docstring(summary='something')
    assert docstr.info['summary'] == 'something'
    docstr = docstring.Docstring(Summary='something')
    assert docstr.info['summary'] == 'something'
    assert_raises(TypeError, docstring.Docstring, summary=['something'])

    # extended, notes, references, examples
    for header in ['extended', 'notes', 'references', 'examples']:
        docstr = docstring.Docstring(**{header: 'something'})
        assert docstr.info[header] == ['something']
        docstr = docstring.Docstring(**{header: ['something']})
        assert docstr.info[header] == ['something']
        docstr = docstring.Docstring(**{header: ('something')})
        assert docstr.info[header] == ['something']

    # parameters, attributes, methods, returns, yields, raises
    for header in ['parameters', 'attributes', 'methods', 'returns', 'yields', 'raises',
                   'other parameters', 'see also']:
        # with types and description
        for contents in (docstring.TabbedInfo(name='param', types=['str', 'int'],
                                              descs='something'),
                         {'name': 'param', 'types': ['str', 'int'], 'descs': 'something'}):

            docstr = docstring.Docstring(**{header: contents})
            assert isinstance(docstr.info[header], list)
            assert isinstance(docstr.info[header][0], docstring.TabbedInfo)
            assert docstr.info[header][0].name == 'param'
            assert docstr.info[header][0].types == ['str', 'int']
            assert docstr.info[header][0].descs == ['something']

        # with signature and description
        for contents in (docstring.TabbedInfo(name='method', signature='(a, b)',
                                              descs='something'),
                         {'name': 'method', 'signature': '(a, b)', 'descs': 'something'}):
            docstr = docstring.Docstring(**{header: contents})
            assert isinstance(docstr.info[header], list)
            assert isinstance(docstr.info[header][0], docstring.TabbedInfo)
            assert docstr.info[header][0].name == 'method'
            assert docstr.info[header][0].signature == '(a, b)'
            assert docstr.info[header][0].descs == ['something']

        # with description
        for contents in (docstring.TabbedInfo(name='method', descs='something'),
                         {'name': 'method', 'descs': 'something'}):
            docstr = docstring.Docstring(**{header: contents})
            assert isinstance(docstr.info[header], list)
            assert isinstance(docstr.info[header][0], docstring.TabbedInfo)
            assert docstr.info[header][0].name == 'method'
            assert docstr.info[header][0].descs == ['something']

    assert_raises(TypeError, docstring.Docstring, parameters='asdfasdf')

    # something random
    docstr = docstring.Docstring(random='desc')
    assert docstr.info['random'] == 'desc'
    assert_raises(TypeError, docstring.Docstring, random=['123123'])


def test_tabbedinfo_init():
    """Tests pydocstring.docstring.TabbedInfo.__init__."""
    # with description
    test = docstring.TabbedInfo('name')
    assert test.name == 'name'
    assert test.descs == []
    test = docstring.TabbedInfo('name', descs='description')
    assert test.name == 'name'
    assert test.descs == ['description']
    test = docstring.TabbedInfo('name', descs=('description1', 'description2'))
    assert test.name == 'name'
    assert test.descs == ['description1', 'description2']
    assert_raises(TypeError, docstring.TabbedInfo, 'name', descs=1)

    # with types and description
    test = docstring.TabbedInfo('name', types='type', descs='description')
    assert test.name == 'name'
    assert test.types == ['type']
    assert test.descs == ['description']
    test = docstring.TabbedInfo('name', types=('type1', 'type2'), descs='description')
    assert test.name == 'name'
    assert test.types == ['type1', 'type2']
    assert test.descs == ['description']
    assert_raises(TypeError, docstring.TabbedInfo, 'name', types=str, descs='description')

    # with signature and description
    test = docstring.TabbedInfo('name', signature='(a, b)', descs='description')
    assert test.name == 'name'
    assert test.signature == '(a, b)'
    assert test.descs == ['description']
    test = docstring.TabbedInfo('name', signature='\na, b ', descs='description')
    assert test.name == 'name'
    assert test.signature == '(a, b)'
    assert test.descs == ['description']
    assert_raises(TypeError, docstring.TabbedInfo, 'name', signature=str, descs='description')

    # with signature, types, and description
    test = docstring.TabbedInfo('name',
                                signature='a, b', types=['str', 'int'], descs='description')
    assert test.name == 'name'
    assert test.signature == '(a, b)'
    assert test.types == ['str', 'int']
    assert test.descs == ['description']
    test = docstring.TabbedInfo('name', signature='\na, b ', types='str', descs='description')
    assert test.name == 'name'
    assert test.types == ['str']
    assert test.signature == '(a, b)'
    assert test.descs == ['description']
    assert_raises(TypeError, docstring.TabbedInfo, 'name', signature=str, descs='description')


def test_tabbedinfo_make_numpy():
    """Tests pydocstring.docstring.TabbedInfo.make_numpy."""
    # description
    info = docstring.TabbedInfo('width',
                                descs='Maximum number of characters allowed in each width')
    assert (info.make_numpy(width=100, indent_level=0, tabsize=4) ==
            'width\n'
            '    Maximum number of characters allowed in each width')
    # description + indentation
    info = docstring.TabbedInfo('width',
                                descs='Maximum number of characters allowed in each width')
    assert (info.make_numpy(width=35, indent_level=0, tabsize=4) ==
            'width\n'
            '    Maximum number of characters\n'
            '    allowed in each width')
    # description + types
    info = docstring.TabbedInfo('width', types='int',
                                descs='Maximum number of characters allowed in each width')
    assert (info.make_numpy(width=100, indent_level=0, tabsize=4) ==
            'width : int\n'
            '    Maximum number of characters allowed in each width')
    info = docstring.TabbedInfo('width', types=['int', 'float'],
                                descs='Maximum number of characters allowed in each width')
    assert (info.make_numpy(width=100, indent_level=0, tabsize=4) ==
            'width : {int, float}\n'
            '    Maximum number of characters allowed in each width')
    # description + types + indentation
    info = docstring.TabbedInfo('width', types=['int', 'float', 'np.int64'],
                                descs='Maximum number of characters allowed in each width')
    assert (info.make_numpy(width=35, indent_level=1, tabsize=4) ==
            '    width : {int, float,\n'
            '                   np.int64}\n'
            '        Maximum number of\n'
            '        characters allowed in each\n'
            '        width')
    # description + signature
    info = docstring.TabbedInfo('width', signature='param1, param2',
                                descs='Maximum number of characters allowed in each width')
    assert (info.make_numpy(width=100, indent_level=0, tabsize=4) ==
            'width(param1, param2)\n'
            '    Maximum number of characters allowed in each width')
    # description + signature + indentation
    info = docstring.TabbedInfo('width', signature='param1, param2, param3, param4',
                                descs='Maximum number of characters allowed in each width')
    assert (info.make_numpy(width=35, indent_level=1, tabsize=4) ==
            '    width(param1, param2,\n'
            '                param3, param4)\n'
            '        Maximum number of\n'
            '        characters allowed in each\n'
            '        width')
    # description + signature + types
    info = docstring.TabbedInfo('width', signature='param1, param2', types='int',
                                descs='Maximum number of characters allowed in each width')
    assert_raises(NotImplementedError, info.make_numpy, width=100, indent_level=0,
                  tabsize=4)


def test_docstring_make_numpy():
    """Tests pydocstring.docstring.Docstring.make_numpy."""
    # summary
    test = docstring.Docstring(
        summary='something happening in this thing, it really happens oh yes it does the thing',
    )
    assert (test.make_numpy(width=100, indent_level=0, tabsize=4) ==
            '"""something happening in this thing, it really happens oh yes it does the thing\n"""')

    # extended
    test = docstring.Docstring(extended='dasfsdf')
    # assert_raises(NotImplementedError, test.make_numpy, width=100, indent_level=0,
    #               tabsize=4)
    assert (test.make_numpy(width=100, indent_level=0, tabsize=4) ==
            '"""\n\ndasfsdf\n"""')

    # parameters, attributes, methods, returns, yields, raises, other parameters, see also
    for header in ['parameters', 'attributes', 'methods', 'returns', 'yields', 'raises',
                   'other parameters', 'see also']:
        # with types and description
        test = docstring.Docstring(**{header: {'name': 'something',
                                               'types': ['sometype1', 'sometype2'],
                                               'descs': ('something happening in this thing, it '
                                                         'really happens oh yes it does '
                                                         'the thing')}})
        assert (test.make_numpy(width=70, indent_level=0, tabsize=4) ==
                '"""\n\n'
                '{0}\n'
                '{1}\n'
                'something : {2}\n'
                '    something happening in this thing, it really happens oh yes it\n'
                '    does the thing\n"""'.format(header.title(), '-' * len(header),
                                                 '{sometype1, sometype2}'))
        # with signature and description
        test = docstring.Docstring(**{header: {'name': 'something',
                                               'signature': 'a, b, c',
                                               'descs': ('something happening in this thing, it '
                                                         'really happens oh yes it does '
                                                         'the thing')}})
        assert (test.make_numpy(width=70, indent_level=0, tabsize=4) ==
                '"""\n\n'
                '{0}\n'
                '{1}\n'
                'something(a, b, c)\n'
                '    something happening in this thing, it really happens oh yes it\n'
                '    does the thing\n"""'.format(header.title(), '-' * len(header),))
        # with description
        test = docstring.Docstring(**{header: {'name': 'something',
                                               'descs': ('something happening in this thing, it '
                                                         'really happens oh yes it does '
                                                         'the thing')}})
        assert (test.make_numpy(width=70, indent_level=0, tabsize=4) ==
                '"""\n\n'
                '{0}\n'
                '{1}\n'
                'something\n'
                '    something happening in this thing, it really happens oh yes it\n'
                '    does the thing\n"""'.format(header.title(), '-' * len(header),))

    # example function
    test = docstring.Docstring(
        summary='Returns something',
        extended='More description',
        parameters={'name': 'x',
                    'types': ['sometype1', 'sometype2'],
                    'descs': 'parameter of the function'},
        returns={'name': 'something',
                 'types': 'str',
                 'descs': 'value of the function at x'},
        raises={'name': 'NotImplementedError'},
        notes=['This function actually does nothing']
    )
    assert (test.make_numpy(width=100, indent_level=0, tabsize=4) ==
            '"""Returns something\n\n'
            'More description\n\n'
            'Parameters\n'
            '----------\n'
            'x : {sometype1, sometype2}\n'
            '    parameter of the function\n\n'
            'Returns\n'
            '-------\n'
            'something : str\n'
            '    value of the function at x\n\n'
            'Raises\n'
            '------\n'
            'NotImplementedError\n\n'
            'Notes\n'
            '-----\n'
            'This function actually does nothing\n'
            '"""')

    # example class
    test = docstring.Docstring(
        summary='Class for doing something.',
        extended='More description',
        attributes={'name': 'x',
                    'types': ['sometype1', 'sometype2'],
                    'descs': 'some attribute'},
        methods={'name': 'f',
                 'signature': '(x)',
                 'descs': 'Does nothing.'},
        notes=['This class actually does nothing'],
        references='some reference'
    )
    assert (test.make_numpy(width=100, indent_level=0, tabsize=4) ==
            '"""Class for doing something.\n\n'
            'More description\n\n'
            'Attributes\n'
            '----------\n'
            'x : {sometype1, sometype2}\n'
            '    some attribute\n\n'
            'Methods\n'
            '-------\n'
            'f(x)\n'
            '    Does nothing.\n\n'
            'Notes\n'
            '-----\n'
            'This class actually does nothing\n\n'
            'References\n'
            '----------\n'
            '.. [1] some reference\n'
            '"""')
