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
