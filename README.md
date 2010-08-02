# python-specfor

A Framework for Behavior Driven Development(BDD) based on stdlib's unittest

- It is inspired from Ruby's RSpec. 
- Spec definition is based on Python decorator description.

## Features

- Python decorator based Spec definition
- "Spec" definition is compatible with unittest.TestCase
- Spec files can execute with unittest or nose
- Markdown document generator from spec file
- RSpec like Expectation (e.g. `the[xxx].should.be[yyy]`) 
- Decorator based Mock generator

## Spec Example

    # spec_sum.py
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


## Resources

- [PyPI python-specfor](http://pypi.python.org/pypi/python-specfor)
- [RSpec](http://rspec.info/)
