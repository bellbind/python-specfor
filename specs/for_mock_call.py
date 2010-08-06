from specfor import the, spec

count_mock_spec = spec.of("mock with count call")
@count_mock_spec.that("count just")
def behavior(its):
    from specfor import mock
    
    counter_mock = mock.define("counter")
    method_def = counter_mock.method("count")
    @method_def.define(at=1)
    def count(self):
        return 1
    
    counter = counter_mock("id-0")
    with the.raising[AssertionError]: mock.check(counter)
    
    counter.count()
    mock.check(counter)
    
    counter.count()
    with the.raising[AssertionError]: mock.check(counter)
    pass

@count_mock_spec.that("count over")
def behavior(its):
    from specfor import mock
    
    counter_mock = mock.define("counter")
    method_def = counter_mock.method("count")
    @method_def.define(over=1)
    def count(self):
        return 1
    
    counter = counter_mock("id-0")
    with the.raising[AssertionError]: mock.check(counter)
    
    counter.count()
    mock.check(counter)
    
    counter.count()
    mock.check(counter)
    pass

@count_mock_spec.that("count until")
def behavior(its):
    from specfor import mock
    
    counter_mock = mock.define("counter")
    method_def = counter_mock.method("count")
    @method_def.define(until=1)
    def count(self):
        return 1
    
    counter = counter_mock("id-0")
    mock.check(counter)
    
    counter.count()
    mock.check(counter)
    
    counter.count()
    with the.raising[AssertionError]: mock.check(counter)
    pass

@count_mock_spec.that("count between")
def behavior(its):
    from specfor import mock
    
    counter_mock = mock.define("counter")
    method_def = counter_mock.method("count")
    @method_def.define(between=(1, 3))
    def count(self):
        return 1
    
    counter = counter_mock("id-0")
    with the.raising[AssertionError]: mock.check(counter)
    
    counter.count()
    mock.check(counter)
    counter.count()
    mock.check(counter)
    counter.count()
    mock.check(counter)
    
    counter.count()
    with the.raising[AssertionError]: mock.check(counter)
    pass


spec.publish(globals())
