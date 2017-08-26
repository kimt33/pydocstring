import pydocstring.docstring
import pydocstring.wrapper


def test_wrapper_docstring_func():
    """Test pydocstring.wrapper.docstring on a function."""
    @pydocstring.wrapper.docstring
    def test():
        """Test docstring.

        Parameters
        ----------
        x : int
            Something.
        """
        pass

    assert test.__doc__ == ('Test docstring.\n'
                            '\n'
                            'Parameters\n'
                            '----------\n'
                            'x : int\n'
                            '    Something.')
    assert hasattr(test, '_docstring')
    assert isinstance(test._docstring, pydocstring.docstring.Docstring)
    assert test._docstring.make_numpy(include_quotes=False) == test.__doc__
    assert test._docstring.info['summary'] == 'Test docstring.'
    assert test._docstring.info['parameters'][0].name == 'x'
    assert test._docstring.info['parameters'][0].types == ['int']
    assert test._docstring.info['parameters'][0].descs == ['Something.']


def test_wrapper_docstring_class():
    """Test pydocstring.wrapper.docstring on a class."""
    @pydocstring.wrapper.docstring
    class Test:
        """Test docstring.

        Attributes
        ----------
        x : int
            Something.
        """
        pass
    test = Test()

    assert test.__doc__ == ('Test docstring.\n'
                            '\n'
                            'Attributes\n'
                            '----------\n'
                            'x : int\n'
                            '    Something.')
    assert hasattr(test, '_docstring')
    assert isinstance(test._docstring, pydocstring.docstring.Docstring)
    assert test._docstring.make_numpy(include_quotes=False) == test.__doc__
    assert test._docstring.info['summary'] == 'Test docstring.'
    assert test._docstring.info['attributes'][0].name == 'x'
    assert test._docstring.info['attributes'][0].types == ['int']
    assert test._docstring.info['attributes'][0].descs == ['Something.']


def test_wrapper_docstring_recursive_func():
    """Test pydocstring.wrapper.docstring_recursive on a function."""
    def test():
        """Test docstring."""
        pass

    def test2():
        """Another docstring."""
        pass
    test.test2 = test2

    def test3():
        """Yet another docstring."""
        pass
    test.test2.test3 = test3

    # NOTE: the pretty decorator @ format cannot be used here because test2 and test3 are assigned
    #       after the creation of the initial object and the decorator is only applied once (near
    #       the creation of test)
    test = pydocstring.wrapper.docstring_recursive(test)

    docstrings = {test: 'Test docstring.',
                  test.test2: 'Another docstring.',
                  test.test2.test3: 'Yet another docstring.'}
    for obj, doc in docstrings.items():
        assert obj.__doc__ == doc
        assert hasattr(obj, '_docstring')
        assert isinstance(obj._docstring, pydocstring.docstring.Docstring)
        assert obj._docstring.make_numpy(include_quotes=False) == obj.__doc__
        assert obj._docstring.info['summary'] == doc


def test_wrapper_docstring_recursive_class():
    """Test pydocstring.wrapper.docstring_recursive on a class."""
    @pydocstring.wrapper.docstring_recursive
    class Test:
        """Some test docstring.

        Take care of gaps
        """
        def f():
            """Some function.

            Gaps?
            """

    test = Test()

    assert test.__doc__ == 'Some test docstring.\n\nTake care of gaps'
    assert hasattr(test, '_docstring')
    assert isinstance(test._docstring, pydocstring.docstring.Docstring)
    assert test._docstring.make_numpy(include_quotes=False) == test.__doc__
    assert test._docstring.info['summary'] == 'kome test docstring.'


def test_wrapper_docstring_func_kwargs():
    """Test pydocstring.wrapper.docstring on a function with keyword arguments."""
    @pydocstring.wrapper.docstring(indent_level=1)
    def f():
        """Test docstring.

        Test extended."""
        pass

    assert f.__doc__ == 'Test docstring.\n\n    Test extended.'

