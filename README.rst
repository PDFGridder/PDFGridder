==========
PDFGridder
==========

PDFGridder.org is a website that allows you to build your grid system and
download it as a PDF, CSS, or InDesign file.

Requirements
============

* Python 2.7
* Pycairo

Configuration
=============

Fill in all your secrets in a ``.env`` file. See the ``env`` file (no initial dot) for a
list of the necessary secrets.

Installation
============

::

    $ pip install -r REQUIREMENTS.txt
    $ ./manage.py migrate
    $ ./manage.py collectstatic


License
=======

This software is relesed under the MIT License.
