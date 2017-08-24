import pydocstring.utils


def test_remove_indent():
    """Test pydocstring.utils.remove_indent."""
    # string input
    assert (pydocstring.utils.remove_indent('   fx\n    gx\n  hx') == '   fx\n  gx\nhx')
    assert (pydocstring.utils.remove_indent('   fx\n    gx\n  hx',
                                            include_firstline=True) == ' fx\n  gx\nhx')
    # list of string input
    assert (pydocstring.utils.remove_indent(['   fx', '    gx', '  hx']) == '   fx\n  gx\nhx')
    assert (pydocstring.utils.remove_indent(['   fx', '    gx', '  hx'],
                                            include_firstline=True) == ' fx\n  gx\nhx')


def test_wrap():
    """Test pydocstring.utils.wrap."""
    assert (pydocstring.utils.wrap('hello my name is', width=5, indent_level=0, tabsize=4)
            == 'hello\nmy\nname\nis')
    assert (pydocstring.utils.wrap('hello my name is', width=5, indent_level=1, tabsize=1)
            == ' hello\n my\n name\n is')
    assert (pydocstring.utils.wrap('\n\nhello   my   name   is\n\n', width=5, indent_level=0,
                                   tabsize=4) == 'hello\nmy\nname\nis')
    assert (pydocstring.utils.wrap('hello my name is', width=5, indent_level=0, tabsize=4,
                                   added_initial_indent='xx')
            == 'xxhello\nmy\nname\nis')
    assert (pydocstring.utils.wrap('hello my name is', width=5, indent_level=0, tabsize=4,
                                   added_subsequent_indent='xx')
            == 'hello\nxxmy\nxxname\nxxis')
    assert (pydocstring.utils.wrap('hello my name is', width=5, indent_level=0, tabsize=4,
                                   edges=('(', ')'))
            == '(hello)\n(my)\n(name)\n(is)')
    assert (pydocstring.utils.wrap('hello my name is', width=11, indent_level=1, tabsize=1,
                                   edges=('(', ')'))
            == ' (hello my)\n (name is)')
    assert (pydocstring.utils.wrap('hello my name is', width=10, indent_level=1, tabsize=1,
                                   edges=('(', ')'))
            == ' (hello)\n (my name)\n (is)')
    assert (pydocstring.utils.wrap('1 2 3 4 5 6 7 8 9 0', width=8, added_subsequent_indent='  ')
            == '1 2 3 4\n  5 6 7\n  8 9 0')
    assert (pydocstring.utils.wrap('1 2 3 4 5 6 7 8 9 0', width=7, added_subsequent_indent='  ')
            == '1 2 3 4\n  5 6 7\n  8 9 0')
    assert (pydocstring.utils.wrap('1 2 3 4 5 6 7 8 9 0', width=7, added_subsequent_indent='  ')
            == '1 2 3 4\n  5 6 7\n  8 9 0')

    # let says we have a string
    start = 'x = ('
    end = ')'

    assert(start + pydocstring.utils.wrap('1 + 2 + 3 + 4 + 5 + 6 + 7',
                                          width=9,
                                          remove_first_indent=True,
                                          added_initial_indent=' '*len(start),
                                          added_subsequent_indent=' '*len(start)) + end ==
           'x = (1 +\n'
           '     2 +\n'
           '     3 +\n'
           '     4 +\n'
           '     5 +\n'
           '     6 +\n'
           '     7)')
    assert(start + pydocstring.utils.wrap('1 + 2 + 3 + 4 + 5 + 6 + 7',
                                          width=12,
                                          remove_first_indent=False,
                                          added_subsequent_indent=' '*len(start)) + end ==
           'x = (1 + 2 + 3\n'
           '     + 4\n'
           '     + 5\n'
           '     + 6\n'
           '     + 7)')
