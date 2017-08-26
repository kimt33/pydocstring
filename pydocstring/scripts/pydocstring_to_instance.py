"""Script for converting the docstrings of a Python file from one format to another.

Methods
-------

"""
import argparse
import os
import re
import shutil
import sys
import pydocstring.docstring
import pydocstring.numpy_docstring
import pydocstring.utils


def extract_docstring(filename):
    """Extract the docstring from a python file.

    Python file is imported and the docstring is extracted from the __doc__ attribute.

    Parameters
    ----------
    filename : str
        Name of the python file

    Returns
    -------
    docstrings : list of str
        List of docstrings found in the python file.

    Raises
    ------
    ValueError
        If there are unpaired (odd number of) triple quotatations.
        If something goes wrong when finding the triple quotations.
    """
    dirname, modulename = os.path.split(filename)
    # add directory to path
    sys.path.insert(0, dirname)
    # import file
    module = __import__(os.path.splitext(modulename)[0])
    # extract members
    members = pydocstring.utils.extract_docstring_module(module, recursive=True).values()

    return [member.__doc__ for member in members]


def replace_docstrings(filename, doc_format, width=None, tabsize=None):
    """Replace the specified docstrings from a file to another docstring.

    Parameters
    ----------
    filename : str
        Name of the file.
    doc_format : {'numpy', 'google', 'rst', 'code'}
        Format of the new docstring.

    Raises
    ------
    ValueError
        If the number of docstrings from `from_docstring` and `to_docstring` does not match.
    NotImplementedError
        If `doc_format` is not 'numpy'
    """
    if width is None:
        width = 100
    if tabsize is None:
        tabsize = 4

    # FIXME: add import
    old_docstrings = extract_docstring(filename)

    # make backup
    shutil.copyfile(filename, filename + '.bak')

    # read code
    with open(filename, 'r') as f:
        code = f.read()

    for old in old_docstrings:
        doc_data = pydocstring.numpy_docstring.parse_numpy(old)
        doc_instance = pydocstring.docstring.Docstring(**doc_data)
        # extract details surrounding docstring (quotes, raw string, indentation)
        re_old = r'( +)(r)?([\'"]+{0}\s*[\'"]+)'.format(re.escape(old))
        details = re.search(re_old, code)
        # FIXME: this will give weird results if given tabsize and tabsize of the file is
        #        different
        indent_level = len(details.group(1)) // tabsize
        is_raw = details.group(2) == 'r'
        if doc_format == 'numpy':
            new = doc_instance.make_numpy(width=width, indent_level=indent_level,
                                          tabsize=tabsize, is_raw=is_raw)
        elif doc_format == 'code':
            new = doc_instance.make_code(width=width, indent_level=indent_level,
                                         tabsize=tabsize)
        else:
            raise NotImplementedError('Only the format numpy is supported at the moment.')
        code = re.sub(re_old, new, code)

    # write code
    with open(filename, 'w') as f:
        f.write(code)


def main():
    # parse arguments
    parser = argparse.ArgumentParser(
        description='Converts existing numpy docstring to another format.'
    )
    parser.add_argument('filename', action='store', nargs='?', default=None, type=str,
                        help='Python file whose docstrings will be converted.')
    parser.add_argument('format', action='store', nargs='?', default='numpy', type=str,
                        help='Format of the generated docstrings.')
    parser.add_argument('--width', action='store', nargs='?', default=None, type=int,
                        dest='width', help='Maximum line length.')
    parser.add_argument('--tabsize', action='store', nargs='?', default=None, type=int,
                        dest='tabsize', help='Number of spaces in a tab.')
    args = parser.parse_args()

    # replace docstrings
    replace_docstrings(args.filename, args.format, width=args.width,
                       tabsize=args.tabsize)
