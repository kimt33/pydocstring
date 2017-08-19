===========
pydocstring
===========
This module is a collection of tools that help create new docstrings and modify existing ones.
The goal is to develop a more universal representation of a docstring and to create links with
existing docstring formats (e.g. NumPy, Google, rst) through parsers and writers.
Then, we can (hopefully) seemlessly convert from one format to another, as well as modify existing
docstrings via operations on this representation.
For example, we can improve upon the docstring inheritance wrapper by controlling which portions of
the docstrings shall be kept or replaced.


Installation
============

.. code-block:: bash

    git clone https://github.com/kimt33/pydocstring.git
    cd pydocstring
    pip install -e ./
