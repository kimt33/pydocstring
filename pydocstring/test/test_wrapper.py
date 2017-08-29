import abc
import pydocstring.docstring
import pydocstring.wrapper


def test_wrapper_docstring_on_func():
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


def test_wrapper_docstring_on_class():
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


def test_wrapper_docstring_recursive_on_func():
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


def test_wrapper_docstring_recursive_on_class():
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
    assert test._docstring.info['summary'] == 'Some test docstring.'


def test_wrapper_docstring_on_func_kwargs():
    """Test pydocstring.wrapper.docstring on a function with keyword arguments."""
    @pydocstring.wrapper.docstring(indent_level=1)
    def test():
        """Test docstring.

        Test extended."""
        pass

    assert test.__doc__ == 'Test docstring.\n\n    Test extended.'
    assert hasattr(test, '_docstring')
    assert isinstance(test._docstring, pydocstring.docstring.Docstring)
    assert test._docstring.make_numpy(include_quotes=False, indent_level=1) == test.__doc__
    assert test._docstring.info['summary'] == 'Test docstring.'
    assert test._docstring.info['extended'] == ['Test extended.']


def test_wrapper_docstring_on_class_kwargs():
    """Test pydocstring.wrapper.docstring on a class with keyword arguments."""
    @pydocstring.wrapper.docstring(indent_level=1)
    class Test:
        """Test docstring.

        Test extended."""
        pass
    test = Test()

    assert test.__doc__ == 'Test docstring.\n\n    Test extended.'
    assert hasattr(test, '_docstring')
    assert isinstance(test._docstring, pydocstring.docstring.Docstring)
    assert test._docstring.make_numpy(include_quotes=False, indent_level=1) == test.__doc__
    assert test._docstring.info['summary'] == 'Test docstring.'
    assert test._docstring.info['extended'] == ['Test extended.']


def test_wrapper_docstring_recursive_on_func_kwargs():
    """Test pydocstring.wrapper.docstring_recursive on a function with keyword arguments."""
    def test():
        """Test docstring.

        Test extended."""
        pass

    def test2():
        """Another docstring."""
        pass

    def test3():
        """One more docstring."""
        pass

    test.test2 = test2
    test.test3 = test3

    # calling the wrapper
    test = pydocstring.wrapper.docstring_recursive(test, indent_level=1)

    docstrings = {test: 'Test docstring.\n\n    Test extended.',
                  test.test2: 'Another docstring.',
                  test.test3: 'One more docstring.'}
    for obj, doc in docstrings.items():
        assert obj.__doc__ == doc
        assert hasattr(obj, '_docstring')
        assert isinstance(obj._docstring, pydocstring.docstring.Docstring)
        assert obj._docstring.make_numpy(include_quotes=False, indent_level=1) == obj.__doc__
    assert test._docstring.info['summary'] == 'Test docstring.'
    assert test._docstring.info['extended'] == ['Test extended.']
    assert test.test2._docstring.info['summary'] == 'Another docstring.'
    assert test.test3._docstring.info['summary'] == 'One more docstring.'


def test_wrapper_docstring_recursive_on_class_kwargs():
    """Test pydocstring.wrapper.docstring_recursive on a class with keyword arguments."""
    @pydocstring.wrapper.docstring_recursive(indent_level=1)
    class Test:
        """Test docstring.

        Test extended."""
        def x():
            """Another docstring."""
            pass
    test = Test()

    assert test.__doc__ == 'Test docstring.\n\n    Test extended.'
    assert hasattr(test, '_docstring')
    assert isinstance(test._docstring, pydocstring.docstring.Docstring)
    assert test._docstring.make_numpy(include_quotes=False, indent_level=1) == test.__doc__
    assert test._docstring.info['summary'] == 'Test docstring.'
    assert test._docstring.info['extended'] == ['Test extended.']
    assert test.x.__doc__ == 'Another docstring.'
    assert hasattr(test.x, '_docstring')
    assert isinstance(test.x._docstring, pydocstring.docstring.Docstring)
    assert test.x._docstring.info['summary'] == 'Another docstring.'


def test_wrapper_docstring_class():
    """Test pydocstring.wrapper.docstring_class."""
    # method
    @pydocstring.wrapper.docstring_class
    class Parent:
        """Test docstring.

        Test extended."""
        def x():
            """Another docstring."""
            pass
    test = Parent()
    assert test.__doc__ == ('Test docstring.\n\n'
                            'Test extended.\n\n'
                            'Methods\n'
                            '-------\n'
                            'x()\n'
                            '    Another docstring.')

    # property
    @pydocstring.wrapper.docstring_class
    class Parent:
        """Test docstring.

        Test extended."""
        @property
        def x():
            """Another docstring."""
            pass
    test = Parent()
    assert test.__doc__ == ('Test docstring.\n\n'
                            'Test extended.\n\n'
                            'Properties\n'
                            '----------\n'
                            'x\n'
                            '    Another docstring.')

    # abstract method
    @pydocstring.wrapper.docstring_class
    class Parent(abc.ABC):
        """Test docstring.

        Test extended."""
        @abc.abstractmethod
        def x():
            """Another docstring."""
            pass
    assert Parent.__doc__ == ('Test docstring.\n\n'
                              'Test extended.\n\n'
                              'Abstract Methods\n'
                              '----------------\n'
                              'x()\n'
                              '    Another docstring.')

    # abstract properties
    @pydocstring.wrapper.docstring_class
    class Parent(abc.ABC):
        """Test docstring.

        Test extended."""
        @abc.abstractproperty
        def x():
            """Another docstring."""
            pass
    assert Parent.__doc__ == ('Test docstring.\n\n'
                              'Test extended.\n\n'
                              'Abstract Properties\n'
                              '-------------------\n'
                              'x\n'
                              '    Another docstring.')

    # inheritance from parent
    @pydocstring.wrapper.docstring_class
    class Parent:
        """Test docstring.

        Test extended."""
        def x():
            """Another docstring."""
            pass

    @pydocstring.wrapper.docstring_class(parent=Parent)
    class Child(Parent):
        """Overwritten docstring."""
        pass

    test = Child()
    assert test.__doc__ == ('Overwritten docstring.\n\n'
                            'Test extended.\n\n'
                            'Methods\n'
                            '-------\n'
                            'x()\n'
                            '    Another docstring.')
