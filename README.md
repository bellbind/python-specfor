# python-specfor

A Framework for Behavior Driven Development(BDD) based on stdlib's unittest

- It is inspired from Ruby's RSpec. 
- Spec definition is based on Python decorator description.

## Features

- Python decorator based Spec definition
- "Spec" definition is compatible with `unittest.TestCase`
- Spec files can execute with `unittest` or `nosetests`
- RSpec like Expectation (e.g. `the[xxx].should.be[yyy]`) 
- Decorator based "Mock" object definition
- All features can be used independently: e.g. use spec with `nose.tools`
- Markdown document generator from spec file

## Install

For install/update, use `easy_install` command:

    easy_install -U python-specfor

## Spec Example

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

For more examples, see: 
[examples/*.py](http://github.com/bellbind/python-specfor/tree/master/examples/)

## Usage

"Spec" code is completely `unittest` code.
It cound run by `unittest` various runners:

    python -m examples.sum_spec

At Python 2.7, "Spec" can run by `python -m unittest` runner command:

    python2.7 -m unittest examples.sum_spec.empty_list

It is also compatible with "nose". so it can run by `nosetests`:

    nosetests examples/sum_spec.py

## License

[GNU Lesser General Public License](http://www.gnu.org/copyleft/lesser.html)

## Authors

- [@bellbind](http://twitter.com/bellbind)

## Resources

- [PyPI python-specfor](http://pypi.python.org/pypi/python-specfor)
- [RSpec](http://rspec.info/)
- [nose](http://somethingaboutorange.com/mrl/projects/nose/)
