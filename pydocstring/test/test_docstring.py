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
            '    width : {int, float, np.int64}\n'
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
            '    width(param1, param2, param3,\n'
            '          param4)\n'
            '        Maximum number of\n'
            '        characters allowed in each\n'
            '        width')
    # description + signature + types
    info = docstring.TabbedInfo('width', signature='param1, param2', types='int',
                                descs='Maximum number of characters allowed in each width')
    assert (info.make_numpy(width=100, indent_level=0, tabsize=4) ==
            'width(param1, param2) : int\n'
            '    Maximum number of characters allowed in each width')


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


def test_docstring_make_code():
    """Tests pydocstring.docstring.Docstring.make_code."""
    # summary
    test = docstring.Docstring(
        summary='something happening in this thing, it really happens oh yes it does the thing',
    )
    assert (test.make_code(width=100, indent_level=0, tabsize=4) ==
            "__doc__ = Docstring(**{\n"
            "    'summary': ('something happening in this thing, it really happens oh yes it does "
            "the thing'),\n"
            "})")

    # extended
    test = docstring.Docstring(extended='dasfsdf')
    assert (test.make_code(width=100, indent_level=0, tabsize=4) ==
            "__doc__ = Docstring(**{\n"
            "    'extended': [\n"
            "        ('dasfsdf')\n"
            "    ],\n"
            "})")
    test = docstring.Docstring(extended=['dasfsdf', 'ffdsfsdf'])
    assert (test.make_code(width=100, indent_level=0, tabsize=4) ==
            "__doc__ = Docstring(**{\n"
            "    'extended': [\n"
            "        ('dasfsdf'),\n"
            "        ('ffdsfsdf')\n"
            "    ],\n"
            "})")

    # parameters, attributes, methods, returns, yields, raises, other parameters, see also
    for header in ['parameters', 'attributes', 'methods', 'returns', 'yields', 'raises',
                   'other parameters', 'see also']:
        # with types and description
        test = docstring.Docstring(**{header: {'name': 'something',
                                               'types': ['sometype1', 'sometype2'],
                                               'descs': ('something happening in this thing, it '
                                                         'really happens oh yes it does '
                                                         'the thing')}})
        assert (test.make_code(width=70, indent_level=0, tabsize=4) ==
                "__doc__ = Docstring(**{\n"
                "    '" + header + "': [\n"
                "        {\n"
                "            'name': ('something'),\n"
                "            'types': ['sometype1', 'sometype2'],\n"
                "            'descs': [\n"
                "                ('something happening in this thing, it really '\n"
                "                 'happens oh yes it does the thing')\n"
                "            ]\n"
                "        }\n"
                "    ],\n"
                "})")
        # with signature and description
        test = docstring.Docstring(**{header: {'name': 'something',
                                               'signature': 'a, b, c',
                                               'descs': ('something happening in this thing, it '
                                                         'really happens oh yes it does '
                                                         'the thing')}})
        assert (test.make_code(width=70, indent_level=0, tabsize=4) ==
                "__doc__ = Docstring(**{\n"
                "    '" + header + "': [\n"
                "        {\n"
                "            'name': ('something'),\n"
                "            'signature': ('(a, b, c)'),\n"
                "            'descs': [\n"
                "                ('something happening in this thing, it really '\n"
                "                 'happens oh yes it does the thing')\n"
                "            ]\n"
                "        }\n"
                "    ],\n"
                "})")
        # with description
        test = docstring.Docstring(**{header: {"name": "something",
                                               "descs": ("something happening in this thing, it "
                                                         "really happens oh yes it does "
                                                         "the thing")}})
        assert (test.make_code(width=70, indent_level=0, tabsize=4) ==
                "__doc__ = Docstring(**{\n"
                "    '" + header + "': [\n"
                "        {\n"
                "            'name': ('something'),\n"
                "            'descs': [\n"
                "                ('something happening in this thing, it really '\n"
                "                 'happens oh yes it does the thing')\n"
                "            ]\n"
                "        }\n"
                "    ],\n"
                "})")

    # example function
    test = docstring.Docstring(
        summary="Returns something",
        extended="More description",
        parameters={"name": "x",
                    "types": ["sometype1", "sometype2"],
                    "descs": "parameter of the function"},
        returns={"name": "something",
                 "types": "str",
                 "descs": "value of the function at x"},
        raises={"name": "NotImplementedError"},
        notes=["This function actually does nothing"]
    )
    assert (test.make_code(width=100, indent_level=0, tabsize=4) ==
            "__doc__ = Docstring(**{\n"
            "    'summary': ('Returns something'),\n"
            "    'extended': [\n"
            "        ('More description')\n"
            "    ],\n"
            "    'parameters': [\n"
            "        {\n"
            "            'name': ('x'),\n"
            "            'types': ['sometype1', 'sometype2'],\n"
            "            'descs': [\n"
            "                ('parameter of the function')\n"
            "            ]\n"
            "        }\n"
            "    ],\n"
            "    'returns': [\n"
            "        {\n"
            "            'name': ('something'),\n"
            "            'types': ['str'],\n"
            "            'descs': [\n"
            "                ('value of the function at x')\n"
            "            ]\n"
            "        }\n"
            "    ],\n"
            "    'raises': [\n"
            "        {\n"
            "            'name': ('NotImplementedError')\n"
            "        }\n"
            "    ],\n"
            "    'notes': [\n"
            "        ('This function actually does nothing')\n"
            "    ],\n"
            "})")

    # example class
    test = docstring.Docstring(
        summary="Class for doing something.",
        extended="More description",
        attributes={"name": "x",
                    "types": ["sometype1", "sometype2"],
                    "descs": "some attribute"},
        methods={"name": "f",
                 "signature": "(x)",
                 "descs": "Does nothing."},
        notes=["This class actually does nothing"],
        references="some reference"
    )
    assert (test.make_code(width=100, indent_level=0, tabsize=4) ==
            "__doc__ = Docstring(**{\n"
            "    'summary': ('Class for doing something.'),\n"
            "    'extended': [\n"
            "        ('More description')\n"
            "    ],\n"
            "    'attributes': [\n"
            "        {\n"
            "            'name': ('x'),\n"
            "            'types': ['sometype1', 'sometype2'],\n"
            "            'descs': [\n"
            "                ('some attribute')\n"
            "            ]\n"
            "        }\n"
            "    ],\n"
            "    'methods': [\n"
            "        {\n"
            "            'name': ('f'),\n"
            "            'signature': ('(x)'),\n"
            "            'descs': [\n"
            "                ('Does nothing.')\n"
            "            ]\n"
            "        }\n"
            "    ],\n"
            "    'notes': [\n"
            "        ('This class actually does nothing')\n"
            "    ],\n"
            "    'references': [\n"
            "        ('some reference')\n"
            "    ],\n"
            "})")


def test_docstring_make_code_specialchar():
    """Test pydocstring.docstring.Docstring.make_code using special characters."""
    # brackets
    test = docstring.Docstring(
        summary="Hello (hi).",
    )
    assert (test.make_code(width=100, indent_level=0, tabsize=4) ==
            "__doc__ = Docstring(**{\n"
            "    'summary': ('Hello (hi).'),\n"
            "})")

    # curly brackets
    test = docstring.Docstring(
        summary="Hello (hi).",
    )
    assert (test.make_code(width=100, indent_level=0, tabsize=4) ==
            "__doc__ = Docstring(**{\n"
            "    'summary': ('Hello (hi).'),\n"
            "})")
    # spaces
    test = docstring.Docstring(
        parameters={'name': 'x', 'types': 'int', 'descs': 'Some number'}
    )
    assert (test.make_code(width=100, indent_level=0, tabsize=4) ==
            "__doc__ = Docstring(**{\n"
            "    'parameters': [\n"
            "        {\n"
            "            'name': ('x'),\n"
            "            'types': ['int'],\n"
            "            'descs': [\n"
            "                ('Some number')\n"
            "            ]\n"
            "        }\n"
            "    ],\n"
            "})")


def test_docstring_inherit():
    """Test pydocstring.docstring.Docstring.inherit."""
    test_one = docstring.Docstring(summary='a')
    test_two = docstring.Docstring(extended='b')
    test_one.inherit(test_two)
    assert test_one.info == {'summary': 'a', 'extended': ['b']}
    assert test_two.info == {'extended': ['b']}

    test_one = docstring.Docstring(summary='a')
    test_two = docstring.Docstring(extended='b')
    test_two.inherit(test_one)
    assert test_one.info == {'summary': 'a'}
    assert test_two.info == {'summary': 'a', 'extended': ['b']}

    test_one = docstring.Docstring(summary='a')
    test_two = docstring.Docstring(summary='b')
    test_one.inherit(test_two)
    assert test_one.info == {'summary': 'a'}

    test_one = docstring.Docstring(parameters={'name': 'a', 'descs': 'one'})
    test_two = docstring.Docstring(parameters={'name': 'b', 'descs': 'two'})
    test_one.inherit(test_two)
    assert test_one.info['parameters'][0].name == 'b'
    assert test_one.info['parameters'][0].descs == ['two']
    assert test_one.info['parameters'][1].name == 'a'
    assert test_one.info['parameters'][1].descs == ['one']

    test_one = docstring.Docstring(parameters={'name': 'a', 'descs': 'one'})
    test_two = docstring.Docstring(parameters={'name': 'a', 'descs': 'two'})
    test_one.inherit(test_two)
    assert test_one.info['parameters'][0].name == 'a'
    assert test_one.info['parameters'][0].descs == ['one']

    test_one = docstring.Docstring(parameters={'name': 'a', 'descs': 'one', 'types': 'int'})
    test_two = docstring.Docstring(parameters={'name': 'a', 'descs': 'one', 'signature': '(x, y)'})
    test_one.inherit(test_two)
    assert test_one.info['parameters'][0].name == 'a'
    assert test_one.info['parameters'][0].descs == ['one']
    assert test_one.info['parameters'][0].types == ['int']
