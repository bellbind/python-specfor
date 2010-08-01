# spec_sum.py
from specfor import the, spec

empty_list = spec.of("empty list")
int_list = spec.of("int list")

@empty_list.before()
def prepare(its):
    its.list = []
    its.sum = 0
    pass

@int_list.before()
def prepare(its):
    its.list = [2, 3, 5, 7, 11]
    its.sum = 28
    pass

@empty_list.that("sum")
@int_list.that("sum")
def sum_spec(its):
    result = sum(its.list)
    the[result].should == its.sum
    pass

spec.publish(globals())
