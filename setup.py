#!/usr/bin/env python
"""A Framework for Behavior Driven Development(BDD) based on stdlib's unittest

It is inspired from Ruby's RSpec. 
Spec definition is based on Python decorator description.

Features
--------

- Python decorator based "Spec" definition
- "Spec" definition is compatible with ``unittest.TestCase``
- Spec files can execute with ``unittest`` or ``nosetests``
- RSpec like Expectation (e.g. ``the[xxx].should.be[yyy]``)
- Decorator based "Mock" object definition
- All features can be used independently: e.g. use spec with ``nose.tools``
- Markdown document generator from spec file


Spec Example
------------

::

    # examples/sum_spec.py
    from specfor import the, spec
    
    empty_list = spec.of("empty list")
    int_list = spec.of("int list")
        
    @empty_list.before()
    def prepare(its):
        its.list = []
        its.sum = 0
    
    @int_list.before()
    def prepare(its):
        its.list = [2, 3, 5, 7, 11]
        its.sum = 28
    
    @empty_list.that("sum")
    @int_list.that("sum")
    def sum_spec(its):
        result = sum(its.list)
        the[result].should == its.sum
    
    spec.publish(globals())

For more detail, see `README.md
<http://github.com/bellbind/python-specfor/blob/master/README.md>`_
"""
doclines = __doc__.split("\n")

classifiers = """
Development Status :: 1 - Planning
Intended Audience :: Developers
License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 3
Topic :: Software Development :: Testing
"""

try:
    from setuptools import setup
    options = {}
    pass
except:
    from distutils.core import setup
    options = {}
    pass

setup(
    name="python-specfor",
    version="0.0.6",
    packages=["specfor", "specfor.mockings", "specfor.mockings.restrictions", 
              "specfor.docs"],
    
    author="bellbind",
    author_email="bellbind@gmail.com",
    url="http://github.com/bellbind/python-specfor",
    license="http://www.gnu.org/copyleft/lesser.html",
    keywords=["bdd", "testing", "unittest"],
    description=doclines[0],
    long_description="\n".join(doclines[2:]),
    classifiers=[ln for ln in classifiers.split("\n") if ln],
    **options
    )
