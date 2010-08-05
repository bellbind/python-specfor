# run test: python -m examples.first
# run nose: nosetest examples/first.py
# generate md doc: python -m specfor.doc examples.first

from specfor import the, spec

empty = spec.of("Empty List")
@empty.before()
def prepare(its):
    its.value = []
    pass

@empty.that("length should be 0")
def behavior(its):
    the[its.value].should.exist
    the[len(its.value)].should.be[0]
    the[its.value].applying(len).should == 0
    pass

@empty.that("length should not be 1")
def behavior(its):
    result = its.value
    with the[result] as it:
        it.applying(len).should.be_in([0, 1, 2])
        it.count("a").should == 0
        the[len(it.value)].should == 0
        pass
    pass

@empty.that("length should not be 1")
def behavior(its):
    the[its.value].applying(repr).should == "[]"
    pass

@empty.that("cannot pop")
def behavior(its):
    with the.raising[IndexError]: 
        its.value.pop()
        pass
    pass

# multiple inputs
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

@nonzeros.that("sum is nonzero")
@zeros.that("sum is zero")
def spec_for_sum(its):
    result = sum([its.a, its.b])
    the[result].should == its.sum
    pass

@nonzeros.before()
def sum_result(its):
    its.sum = 110
    pass
@zeros.before()
def sum_result(its):
    its.sum = 0
    pass


spec.publish(globals())
