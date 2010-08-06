# specs.for_match_plugin

## match plugin

### [match plugin] add new verb

<pre>
@spec_for_match_plugin.that("add new verb")
def behavior(its):
    # refreshed module
    import specfor
    new_specfor = specfor.new_specfor()
    spec = new_specfor.spec
    the = new_specfor.the
    match = new_specfor.match
    # define
    
    class MatchNotInstance(match.MatchAction):
        def __call__(self, expected):
            message = "it[%s] should not be instance of %s" % (
                repr(self.expectation.value), repr(expected))
            assert not isinstance(self.expectation.value, expected), message
            pass
        pass
    match.register(
        "not_be_instance_of",
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
    
    the[spec.run(success_spec).wasSuccessful()].should.be_ok
    the[spec.run(fail_spec).wasSuccessful()].should.be_no
    pass
</pre>
<pre>
@spec_for_match_plugin.after()
def check_clean_env(its):
    from specfor.match import MatchActions
    the["not_be_instance_of"].should.not_be_in[dir(MatchActions)]
    pass
</pre>



