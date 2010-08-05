import specfor

spec_for_match_plugin = specfor.spec.of("match plugin")
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
    success_spec = specfor.spec.of("not instance")
    @success_spec.that("the[val].should.not_be_instance_of[exp_type]")
    def behavior(it):
        specfor.the[{}].should.not_be_instance_of[list]
        pass
    
    fail_spec = specfor.spec.of("not instance")
    @fail_spec.that("the[val].should.not_be_instance_of[exp_type]")
    def behavior(it):
        specfor.the[{}].should.not_be_instance_of[dict]
        pass
    
    r = run_as_tests(success_spec)
    specfor.the[r.wasSuccessful()].should.be_true
    r = run_as_tests(fail_spec)
    specfor.the[r.wasSuccessful()].should.be_false
    pass

@spec_for_match_plugin.after()
def cleanup(its):
    global specfor
    old = specfor
    specfor = specfor.refresh()
    specfor.the[id(specfor)].should != id(old)
    
    from specfor.match import MatchActions
    assert "not_be_instance_of" not in dir(MatchActions)
    pass



def run_as_tests(spec, r=None):
    import unittest
    r = r or unittest.TestResult()
    for name in [n for n in dir(spec) if n.startswith("test")]:
        test = spec(name)
        test.run(r)
        pass
    return r

specfor.spec.publish(globals())

