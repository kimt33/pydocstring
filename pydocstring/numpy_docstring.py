import re
from pydocstring.utils import remove_indent, extract_math, is_math



def parse_numpy(docstring, contains_quotes=False):
    """Extract numpy docstring as a dictionary.

    Multiple descriptions of the indented information (e.g. parameters, attributes, methods,
    returns, yields, raises, see also) are distinguished from one another with a period.
    If the period is not present, then the description is assumed to be a multiline description.

    Parameters
    ----------
    docstring : str
        Numpy docstring.
    contains_quotes : bool
        True if docstring contains \"\"\" or \'\'\'.

    Returns
    -------
    output : dict
        Contents of the docstring separated into different section.
        If the section is summary, then the value is string.
        If the section is extended, notes, references, or examples, then the value is list of
        strings.
        If the section is parameters, other parameters, attributes, methods, returns, yields,
        raises, or see also, then the value is a dictionary with keys 'name', 'signature', 'types',
        or 'docs', with corresonding values string, string, list of strings, and list of strings,
        respectively.
        Otherwise, the values is a list of strings.

    Raises
    ------
    ValueError
        If summary is not in the first or second line.
        If summary is now followed with a blank line.
        If number of '-' does not match the number of characters in the header.
        If given entry of the tabbed information (parameters, attributes, methods, returns, yields,
        raises, see also) had an unexpected pattern.
    NotImplementedError
        If quotes corresponds to a raw string, i.e. r\"\"\".
    """
    docstring = remove_indent(docstring, include_firstline=contains_quotes)

    # remove quotes from docstring
    if contains_quotes:
        quotes = r'[\'\"]{3}'
        if re.search(r'^r{0}'.format(quotes), docstring):
            raise NotImplementedError('A raw string quotation, i.e. r""" cannot be given as a '
                                      'string, i.e. from reading a python file as a string, '
                                      'because the backslashes belonging to escape sequences '
                                      'cannot be distinguished from those of normal backslash.'
                                      'You either need to change existing raw string to normal '
                                      'i.e. convert all occurences of \\ to \\\\, or import the '
                                      'docstring from the instance through `__doc__` attribute.')
    else:
        quotes = r''
    docstring = re.sub(r'^{0}'.format(quotes), '', docstring)
    docstring = re.sub(r'{0}$'.format(quotes), '', docstring)

    output = {}
    # summary
    for regex in [r'^\n?(.*?)\n\n+', r'^\n?(.*?)\n*$']:
        re_summary = re.compile(regex)
        try:
            output['summary'] = re_summary.search(docstring).group(1)
            break
        except AttributeError:
            pass
    else:
        raise ValueError('The summary must be in the first or the second line with a blank line '
                         'afterwards.')
    # remove summary from docstring
    docstring = re_summary.sub('', docstring)
    if docstring == '':
        return output

    # if headers do not exist
    if re.search(r'(\w+)\n(-+)\n+', docstring) is None:
        # split into blocks by math equations and multiple newlines
        extended = [[lines] if is_math(lines) else re.split(r'\n\n+', lines)
                    for lines in extract_math(docstring)]
        extended = [line for lines in extended for line in lines]
        for block in extended:
            if block == '':
                continue
            if not is_math(block):
                # remove quotes
                block = re.sub(r'\n*{0}$'.format(quotes), '', block)
                # remove trailing newlines
                block = re.sub(r'\n+$', '', block)
                # replace newlines
                block = block.replace('\n', ' ')

            output.setdefault('extended', []).append(block)
        return output

    # split docstring by the headers
    split_docstring = re.split(r'\n*(.+)\n(-+)\n+', docstring)
    # check for extended summary
    if re.search(r'^-+$', split_docstring[2]):
        extended, *split_docstring = split_docstring
        # add extended
        extended = [block for block in re.split(r'\n\n+', extended) if block != '']
        # remove newlines
        extended = [block.replace('\n', ' ') for block in extended]
        if extended != []:
            output['extended'] = extended

    for header, lines, contents in zip(split_docstring[0::3],
                                       split_docstring[1::3],
                                       split_docstring[2::3]):
        contents = re.sub(r'\n+$', r'\n', contents)

        if len(header) != len(lines):
            raise ValueError('Need {0} of `-` underneath the header title, {1}'
                             ''.format(len(header), header))

        header = header.lower()
        # special headers (special format for each entry)
        if header in ['parameters', 'other parameters', 'attributes', 'methods', 'returns',
                      'yields', 'raises', 'see also', 'properties', 'abstract properties',
                      'abstract methods']:
            entries = (entry for entry in re.split(r'\n(?!\s+)', contents) if entry != '')
            # FIXME: following regular expression would work only if docstring has spaces adjacent
            #        to ':'
            re_entry = re.compile(r'^(.+?)(\(.+?\))?(?: *: *(.+))?(?:\n|$)')
            for entry in entries:
                if len(re_entry.split(entry)) != 5:
                    raise ValueError('Something went wrong. Could not process the following entry:'
                                     '\n{0}'.format(entry))

                # keep only necessary pieces
                _, name, signature, types, descs = re_entry.split(entry)

                # process signature
                if signature is None:
                    signature = ''
                else:
                    signature = ', '.join(i.strip() for i in signature.split(','))

                # process types
                if types is None:
                    types = []
                elif re.search(r'\{.+\}', types):
                    types = re.search(r'^\{((?:(.+?),\s*)*(.+?))\}$', types).group(1)
                    types = re.split(r',\s*', types)
                else:
                    types = re.search(r'^((?:(.+?),\s*)*(.+?))$', types).group(1)
                    types = re.split(r',\s*', types)
                types = [i for i in types if i is not None]

                # process documentation
                descs = remove_indent(descs, include_firstline=True)
                # NOTE: period is used to terminate a description. i.e. one description is
                #       distinguished from another with a period and a newline.
                descs = re.split(r'\.\n+', descs)
                # add period (only the last line is not missing the period)
                descs = [line + '.' for line in descs[:-1]] + descs[-1:]
                # extract equations
                descs = [line for lines in descs for line in extract_math(lines)]
                # non math blocks will replace newlines with spaces.
                # FIXME: math regex is required here to check if entry is math equation
                descs = [line if is_math(line) else line.replace('\n', ' ') for line in descs]

                # store
                output.setdefault(header, []).append({'name': name})
                if types != []:
                    output[header][-1]['types'] = types
                if signature != '':
                    output[header][-1]['signature'] = signature
                if descs != []:
                    output[header][-1]['descs'] = descs
        else:
            output[header] = [i for i in re.split(r'\n\n+', contents) if i != '']

    return output
