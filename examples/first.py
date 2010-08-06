# run test: python -m examples.first
# run nose: nosetest examples/first.py
# generate md doc: python -m specfor.doc examples.first

# import
from __future__ import with_statement
from specfor import the, spec


# [Ex1] describe a spec
empty = spec.of("Empty List")
# prepare sample data
@empty.before()
def prepare(its):
    its.value = []
    pass

# define behavior
@empty.that("length should be 0")
def behavior(its):
    result = len(its.value)
    # describe expectations for 
    the[result].should.exist
    the[result].should.be[0]
    the[result].applying(str).should == "0"
    pass

@empty.that("length should not be 1")
def behavior(its):
    result = its.value
    # other style of expectations
    with the[result] as it:
        it.should.exist
        it.should.not_be[1]
        it.applying(str).startswith("1").should.be_false
        pass
    pass

@empty.that("cannot pop")
def behavior(its):
    # expect raising error
    with the.raising[IndexError]: 
        its.value.pop()
        pass
    pass

# [Ex2] describe behavior with multiple input patterns
nonzeros = spec.of("non zero values")
@nonzeros.before()
def values(its):
    its.a = 10
    its.b = 100
    pass

zeros = spec.of("zero values")
@zeros.before()
def values(its):
    its.a = 0
    its.b = 0
    pass

# specs share behavior 
@nonzeros.that("sum is nonzero")
@zeros.that("sum is zero")
def spec_for_sum(its):
    result = sum([its.a, its.b])
    the[result].should == its.sum
    pass

# prepare lack data for the behavior
@nonzeros.before()
def sum_result(its):
    its.sum = 110
    pass
@zeros.before()
def sum_result(its):
    its.sum = 0
    pass


# [at last] it makes unittest execution
spec.publish(globals())
