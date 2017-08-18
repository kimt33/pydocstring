import docstring

a = docstring.ParamDocstring('xyz', types=['str'], docs=['something that works'])
print(a.make_numpy(indent_level=1))
