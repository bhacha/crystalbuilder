Getting Started
================


Installation
--------------
This will walk you through installing crystalbuilder. The process is the same regardless of your operating system, but MPB/MEEP are not available on Windows.

1. :ref:`Download <download>`
2. :ref:`Install <install>`
3. :ref:`Examples <examples>`

.. _download:
Download
---------
The most up-to-date version of crystalbuilder can be downloaded from the development branch of `the GitHub repository`_.

It is also available `on PyPI`_ and can be installed using pip:
``pip install crystalbuilder``

.. _the GitHub repository: https://github.com/bhacha/crystalbuilder/tree/development
.. _on PyPI: https://pypi.org/project/crystalbuilder/

.. _install:
Install
--------
Installation in both methods can be done via pip. For the released versions, ``pip install crystalbuilder`` does everything you need. For GitHub downloads, navigate to the download directory and run ``pip install ./crystalbuilder``. That's it (mostly)!

The features in the ``bilbao`` module use data from the Bilbao Crystallographic Server, which is now protected by a CloudFlare check. This means it's best to do a one-time download of the generators and k-vectors for all 230 space groups.


.. _examples:
Examples
---------