.. DemoUnit documentation master file, created by
   sphinx-quickstart on Wed Nov 13 09:51:19 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=======================================================
Welcome to DemoUnit's documentation
=======================================================

A SciUnit library for data-driven testing of electrophysiological features extracted from computational models.

Contents
========
.. toctree::
   :numbered:
   :maxdepth: 1

   {% if test_json|length != 0 %}
   page_testLibrary
   {% endif %}
   page_tests
   page_capabilities
   page_acknowledgement


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
