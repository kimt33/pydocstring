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
    # tab indents
    assert (pydocstring.utils.wrap('hello my name is', width=5, indent_level=0, tabsize=4)
            == 'hello\nmy\nname\nis')
    assert (pydocstring.utils.wrap('hello my name is', width=5, indent_level=1, tabsize=1)
            == ' hello\n my\n name\n is')
    assert (pydocstring.utils.wrap('\n\nhello   my   name   is\n\n', width=5, indent_level=0,
                                   tabsize=4) == 'hello\nmy\nname\nis')
    # added indents
    assert (pydocstring.utils.wrap('hello my name is', width=5, indent_level=0, tabsize=4,
                                   added_indent=['xx', ''])
            == 'xxhello\nmy\nname\nis')
    assert (pydocstring.utils.wrap('hello my name is', width=5, indent_level=0, tabsize=4,
                                   added_indent=['', 'xx'])
            == 'hello\nxxmy\nxxname\nxxis')
    assert (pydocstring.utils.wrap('hello my name is', width=5, indent_level=0, tabsize=4,
                                   added_indent=['xx'])
            == 'xxhello\nxxmy\nxxname\nxxis')
    assert (pydocstring.utils.wrap('hello my name is', width=5, indent_level=0, tabsize=4,
                                   added_indent='xx')
            == 'xxhello\nxxmy\nxxname\nxxis')
    # NOTE: Since break_long_words is false, words that are greater than the width are not broken
    #       into smaller pieces.
    # edges
    assert (pydocstring.utils.wrap('hello my name is', width=5, indent_level=0, tabsize=4,
                                   edges=('(', ')'))
            == '(hello)\n(my)\n(name)\n(is)')
    assert (pydocstring.utils.wrap('hello my name is', width=11, indent_level=1, tabsize=1,
                                   edges=('(', ')'))
            == ' (hello my)\n (name is)')
    assert (pydocstring.utils.wrap('hello my name is', width=10, indent_level=1, tabsize=1,
                                   edges=('(', ')'))
            == ' (hello)\n (my name)\n (is)')
    # remove initial indent
    start = 'x = ('
    end = ')'
    assert(start + pydocstring.utils.wrap('1 + 2 + 3 + 4 + 5 + 6 + 7',
                                          width=9,
                                          remove_initial_indent=True,
                                          added_indent=' '*len(start)) + end == ('x = (1 +\n'
                                                                                 '     2 +\n'
                                                                                 '     3 +\n'
                                                                                 '     4 +\n'
                                                                                 '     5 +\n'
                                                                                 '     6 +\n'
                                                                                 '     7)'))
    assert(start + pydocstring.utils.wrap('1 + 2 + 3 + 4 + 5 + 6 + 7',
                                          width=9,
                                          remove_initial_indent=False,
                                          added_indent=('', ' '*len(start))) + end ==
           ('x = (1 + 2 + 3\n'
            '     + 4\n'
            '     + 5\n'
            '     + 6\n'
            '     + 7)'))
    assert(start + pydocstring.utils.wrap('1 + 2 + 3 + 4 + 5 + 6 + 7',
                                          width=9,
                                          remove_initial_indent=False,
                                          added_indent=' '*len(start)) + end ==
           ('x = (     1 +\n'
            '     2 +\n'
            '     3 +\n'
            '     4 +\n'
            '     5 +\n'
            '     6 +\n'
            '     7)'))
