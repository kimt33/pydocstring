import re
from pydocstring.utils import remove_indent


def parse_numpy(docstring, contains_quotes=False):
    """Extract numpy docstring as a dictionary.

    Parameters
    ----------
    docstring : str
        Numpy docstring.
    contains_quotes : bool
        True if docstring contains \"\"\" or \'\'\'.
    """
    docstring = remove_indent(docstring, include_firstline=contains_quotes)
    quotes = r'[\'"]{3}' if contains_quotes else ''

    # remove first quotes from docstring
    docstring = re.sub(r'^{0}'.format(quotes), '', docstring)

    output = {}
    # summary
    try:
        re_summary = re.compile(r'^(.+?)\n\n+'.format(quotes))
        output['summary'] = re_summary.search(docstring).group(1)
    except AttributeError:
        re_summary = re.compile(r'^\n(.+?)\n\n+'.format(quotes))
        output['summary'] = re_summary.search(docstring).group(1)
    # remove summary from docstring
    docstring = re_summary.sub('', docstring)

    # split docstring by the headers
    split_docstring = re.split(r'(\w+)\n(-+)\n+', docstring)[1:]
    # if extended summary exists
    if re.search(r'^-+$', split_docstring[2]):
        extended, split_docstring = split_docstring[0], split_docstring[1:]
        # add extended
        output['extended'] = re.split(r'\n\n+', extended)

    if len(split_docstring) % 3 != 0:
        raise ValueError('Something went wrong. Are you sure the docstring is set up properly? '
                         'There should be headers in the following format:'
                         'Header\n------')
    for header, lines, contents in zip(split_docstring[0::3],
                                       split_docstring[1::3],
                                       split_docstring[2::3]):
        contents = re.sub(r'\n+$', r'\n', contents)

        if len(header) != len(lines):
            raise ValueError('Need {0} number of `-` underneath the header title, {1}'
                             ''.format(len(header), header))

        header = header.lower()
        if header in ['parameters', 'other parameters', 'attributes', 'methods', 'returns',
                      'yields', 'raises', 'see also']:
            entries = re.split(r'\n(?!\s+)', contents)[:-1]
            re_param = re.compile(r'^(.+?)\s*:\s*(.*?)\n')
            re_method = re.compile(r'^(.+?)(\(.*?\))\n')
            re_other = re.compile(r'^(.+?)\n')
            for entry in entries:
                # parameter like output
                if len(re_param.split(entry)) > 1:
                    name, types, docs = re_param.split(entry)[1:]
                    # proces types
                    if re.search(r'\{.+\}', types):
                        types = re.search(r'\{(?:(.+?),\s*)*(.+?)\}', types).groups()
                    else:
                        types = re.search(r'(?:(.+?),\s*)*(.+?)$', types).groups()
                    types = [i for i in types if i is not None]
                    # store name and types
                    output.setdefault(header, []).append({'name': name, 'types': types})
                # method like output
                elif len(re_method.split(entry)) > 1:
                    name, signature, docs = re_method.split(entry)[1:]
                    # process signature
                    signature = ', '.join(i.strip() for i in signature.split(','))
                    # store name and signature
                    output.setdefault(header, []).append({'name': name, 'signature': signature})
                # others
                else:
                    name, docs = re_other.split(entry)[1:]
                    # store name
                    output.setdefault(header, []).append({'name': name})

                # process documentation
                docs = remove_indent(docs, include_firstline=True)
                docs = re.split(r'\.\n+', docs)
                # add period (only the last line is not missing the period)
                docs = [line + '.' for line in docs[:-1]] + docs[-1:]
                # extract equations
                re_math = re.compile(r'(\.\.\s*math::\n+(?:\s+.+\n)+)\n*')
                docs = [re_math.split(line) for line in docs]
                docs = [line for lines in docs for line in lines if line != '']
                # replace newlines with spaces.
                docs = [line if re_math.search(line) else re.sub('\n', ' ', line) for line in docs]
                # store docs
                output[header][-1]['docs'] = docs
        else:
            output[header] = [i for i in re.split(r'\n\n+', contents) if i != '']

    return output
