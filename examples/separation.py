# [design] separation of behavior and type
# not yet implemented
from specfor import the, spec

# behaviors
seq_spec = spec.behaviors_of("sequence")
@seq_spec.that("sum")
def behavior(its):
    result = sum(its.target)
    the[result].should == its.expected_sum
    pass
@seq_spec.that("any")
def behavior(its):
    result = any(its.target)
    the[result].should == its.expected_any
    pass


list_spec = spec.behaviors_of("list")
@list_spec.that("append/pop")
def behavior(its):
    its.target.append(its.item)
    result = its.target.pop()
    the[result].should == its.item
    pass


# type example
empty_list = spec.of("empty list")
@empty_list.before()
def define(its):
    its.target = []
    pass
@empty_list.of(seq_spec)
def prepare(its):
    its.expected_sum = 0
    its.expected_any = False
    pass
@empty_list.of(list_spec)
def prepare(its):
    its.item = "something"
    pass


int_tuple = spec.of("int tuple")
@int_tuple.before()
def define(its):
    its.target = (2, 3, 5, 7, 11)
    pass
@int_tuple.of(seq_spec)
def prepare(its):
    its.expected_sum = 28
    its.expected_any = True
    pass

spec.publish(globals())
