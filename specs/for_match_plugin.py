from specfor import the, spec


spec_for_match_plugin = spec.of("match plugin")
@spec_for_match_plugin.that("add new verb")
def behavior(its):
    # define
    from specfor.match import MatchAction, register
    
    class MatchNotInstance(MatchAction):
        def __call__(self, expected):
            message = "it[%s] should not be instance of %s" % (
                repr(self.expectation.value), repr(expected))
            assert not isinstance(self.expectation.value, expected), message
            pass
        pass
    register("not_be_instance_of",
             property(lambda self: MatchNotInstance(self.expectation)))
    
    # use
    success_spec = spec.of("not instance")
    @success_spec.that("the[val].should.not_be_instance_of[exp_type]")
    def behavior(it):
        the[{}].should.not_be_instance_of[list]
        pass
    
    fail_spec = spec.of("not instance")
    @fail_spec.that("the[val].should.not_be_instance_of[exp_type]")
    def behavior(it):
        the[{}].should.not_be_instance_of[dict]
        pass
    
    r = run_as_tests(success_spec)
    assert r.wasSuccessful()
    r = run_as_tests(fail_spec)
    assert not r.wasSuccessful()
    pass

    pass

def run_as_tests(spec, r=None):
    import unittest
    r = r or unittest.TestResult()
    for name in [n for n in dir(spec) if n.startswith("test")]:
        test = spec(name)
        test.run(r)
        pass
    return r
spec.publish(globals())

