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
    assert (pydocstring.utils.wrap('hello', indent_level=0, tabsize=4, edges=("'", "'"),
                                   remove_initial_indent=True, added_indent='  ')
            == "'hello'")
    assert (pydocstring.utils.wrap('hello my name is', width=7, indent_level=0, tabsize=4,
                                   edges=("'", "'"))
            ==
            "'hello'\n"
            "' my '\n"
            "'name '\n"
            "'is'")
    assert (pydocstring.utils.wrap('hello my name is', width=11, indent_level=1, tabsize=1,
                                   edges=("'", "'"))
            ==
            " 'hello my'\n"
            " ' name is'")
    assert (pydocstring.utils.wrap('hello my name is', width=10, indent_level=1, tabsize=1,
                                   edges=("'", "'"))
            ==
            " 'hello '\n"
            " 'my name'\n"
            " ' is'")
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


def test_multi_wrap():
    """Test pydocstring.utils.multi_wrap."""
    assert (pydocstring.utils.multi_wrap('a b c d \n  a b c d \n    a b c d ', width=6) ==
            'a b c\nd\n  a b\n  c d\n    a\n    b\n    c\n    d')
    assert (pydocstring.utils.multi_wrap('a b c d \n  a b c d \n    a b c d ', width=8, tabsize=2,
                                         indent_level=1) ==
            '  a b c\n  d\n    a b\n    c d\n      a\n      b\n      c\n      d')
    assert (pydocstring.utils.multi_wrap('a b c d \n  a b c d \n    a b c d ', width=8, tabsize=1,
                                         indent_level=2) ==
            '  a b c\n  d\n    a b\n    c d\n      a\n      b\n      c\n      d')


def test_is_math():
    """Test pydocstring.utils.is_math."""
    assert pydocstring.utils.is_math('.. math::\n\n    x&=2\\\\\n    &=3')
    assert pydocstring.utils.is_math('.. math::\n\n    x&=2\\\\\n    &=3\n')
    assert pydocstring.utils.is_math('\n.. math::\n\n    x&=2\\\\\n    &=3\n\n\n')
    assert not pydocstring.utils.is_math('x\n.. math::\n\n    x&=2\\\\\n    &=3\n\n\n')
    assert pydocstring.utils.is_math('.. math::\n\n    x=2')


def test_extract_math():
    """Test pydocstring.utils.extract_math."""
    assert (pydocstring.utils.extract_math('.. math::\n\n    x &= 2\\\\\n    &= 3\n') ==
            ['.. math::\n\n    x &= 2\\\\\n    &= 3'])
    assert (pydocstring.utils.extract_math('x\n.. math::\n\n    x &= 2\\\\\n    &= 3\n') ==
            ['x', '.. math::\n\n    x &= 2\\\\\n    &= 3'])
    assert (pydocstring.utils.extract_math('x\n.. math::\n\n    x &= 2\\\\\n    &= 3\n\n\n') ==
            ['x', '.. math::\n\n    x &= 2\\\\\n    &= 3'])
    assert (pydocstring.utils.extract_math('x\n.. math::\n\n    x &= 2\\\\\n    &= 3\n\ny') ==
            ['x', '.. math::\n\n    x &= 2\\\\\n    &= 3', 'y'])


def test_layered_wrap():
    """Test pydocstring.utils.layered_wrap."""
    assert (pydocstring.utils.layered_wrap({('[', ']', False): ['hello']})
            == "['hello']")
    assert (pydocstring.utils.layered_wrap({('[', ']', True): ['hello']})
            ==
            "[\n"
            "    'hello'\n"
            "]")
    assert (pydocstring.utils.layered_wrap({('[', ']', False): ['hello', 'hi']})
            == "['hello', 'hi']")
    assert (pydocstring.utils.layered_wrap({('[', ']', True): ['hello', 'hi']})
            ==
            "[\n"
            "    'hello',\n"
            "    'hi'\n"
            "]")
    assert(pydocstring.utils.layered_wrap({('[', ']', True): [{('(', ')', True): ['hello', 'hi']},
                                                              {('x', 'x', False): ['bye']}]})
           ==
           "[\n"
           "    (\n"
           "        'hello',\n"
           "        'hi'\n"
           "    ),\n"
           "    x'bye'x\n"
           "]")
    assert(pydocstring.utils.layered_wrap({('[', ']', False): [{('(', ')', True): ['hello', 'hi']},
                                                               {('x', 'x', False): ['bye']}]})
           ==
           "[(\n"
           "    'hello',\n"
           "    'hi'\n"
           "), x'bye'x]")
    assert(pydocstring.utils.layered_wrap({('[', ']', False): [{('(', ')', False): ['hello', 'hi']},
                                                               {('x', 'x', True): ['bye']}]})
           ==
           "[('hello', 'hi'), x\n"
           "    'bye'\n"
           "x]")
    assert(pydocstring.utils.layered_wrap({('[', ']', True): ['adfs',
                                                              {('(', ')', True): ['hello', 'hi']},
                                                              {('x', 'x', False): ['bye']}]})
           ==
           "[\n"
           "    'adfs',\n"
           "    (\n"
           "        'hello',\n"
           "        'hi'\n"
           "    ),\n"
           "    x'bye'x\n"
           "]")

    # wrap
    assert(pydocstring.utils.layered_wrap({('xy', 'z', False): ['1 2 3 4 5 6 7 8 9 0']},
                                          width=10)
           ==
           "xy'1 2 3 '\n"
           "  '4 5 6 '\n"
           "  '7 8 9 '\n"
           "  '0'z")
    assert(pydocstring.utils.layered_wrap({('xy', 'z', True): ['1 2 3 4 5 6 7 8 9 0']},
                                          width=10)
           ==
           "xy\n"
           "    '1 2 '\n"
           "    '3 4 '\n"
           "    '5 6 '\n"
           "    '7 8 '\n"
           "    '9 0'\n"
           "z")
    assert(pydocstring.utils.layered_wrap({('[', ']', False): ['hello my name is something seven']},
                                          width=19)
           ==
           "['hello my name is'\n"
           " ' something seven']")

    assert(pydocstring.utils.layered_wrap({('[', ']', True): ['hello my name is something seven']},
                                          width=19)
           ==
           "[\n"
           "    'hello my name'\n"
           "    ' is something'\n"
           "    ' seven'\n"
           "]")
    assert(pydocstring.utils.layered_wrap({('[', ']', True): ['this is an example',
                                                              {('(', ')', True): ['hello hi']},
                                                              {('x', 'x', True): ['bye bye']}]},
                                          width=15)
           ==
           "[\n"
           "    'this is '\n"
           "    'an '\n"
           "    'example',\n"
           "    (\n"
           "        'hello'\n"
           "        ' hi'\n"
           "    ),\n"
           "    x\n"
           "        'bye '\n"
           "        'bye'\n"
           "    x\n"
           "]")

    # FIXME: bug
    # assert(pydocstring.utils.layered_wrap({('[', ']', False):
    #                                        ['this is an example',
    #                                         {('(', ')', False): ['hello hi how']},
    #                                         {('x', 'x', False): ['bye bye']}]},
    #                                       width=15)
    #        ==
    #        "['this is an'\n"
    #        " 'example',\n"
    #        " ('hello hi'\n"
    #        "  'how'),\n"
    #        " x'bye bye'x]")

    # FIXME: another bug
    # cannot go from false to true
    assert(pydocstring.utils.layered_wrap({('[', ']', False): {('(', ')', True): 'damn'}},
                                          indent_level=1)
           ==
           "    [(\n"
           "        'damn'\n"
           "    )]")
