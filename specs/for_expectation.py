from specfor import spec


spec_for_expect = spec.of("expectation")
@spec_for_expect.that("for raising error")
def behavior(its):
    from specfor import the
    
    success_spec = spec.of("for raise error")
    @success_spec.that("with the.raising[exception]: do_raise_error()")
    def behavior(it):
        with the.raising[KeyError]:
            {}["abc"]
            pass
        pass
    
    fail_spec = spec.of("for raise error")
    @fail_spec.that("with the.raising[exception]: do_raise_error()")
    def behavior(it):
        with the.raising[KeyError]:
            pass
        pass
    
    
    assert spec.run(success_spec).wasSuccessful()
    assert not spec.run(fail_spec).wasSuccessful()
    pass


@spec_for_expect.that("for equality")
def behavior(its):
    from specfor import the
    
    success_spec = spec.of("equality")
    @success_spec.that("the[val].should.be[exp]")
    def behavior(it):
        the["a" + "b"].should.be["ab"]
        pass
    @success_spec.that("the[val].should == exp")
    def behavior(it):
        the["a" + "b"].should == "ab"
        pass
    
    fail_spec = spec.of("equality")
    @fail_spec.that("the[val].should.be[exp]")
    def behavior(it):
        the["a" + "b"].should.be["abc"]
        pass
    @fail_spec.that("the[val].should == exp")
    def behavior(it):
        the["a" + "b"].should == "abc"
        pass
    
    assert spec.run(success_spec).wasSuccessful()
    assert len(spec.run(fail_spec).failures) == 2
    pass


@spec_for_expect.that("for inequality")
def behavior(its):
    from specfor import the
    
    success_spec = spec.of("inequality")
    @success_spec.that("the[val].should.not_be[exp]")
    def behavior(it):
        the["a" + "b"].should.not_be["abc"]
        pass
    @success_spec.that("the[val].should != exp")
    def behavior(it):
        the["a" + "b"].should != "abc"
        pass
    
    fail_spec = spec.of("inequality")
    @fail_spec.that("the[val].should.not_be[exp]")
    def behavior(it):
        the["a" + "b"].should.not_be["ab"]
        pass
    @fail_spec.that("the[val].should == exp")
    def behavior(it):
        the["a" + "b"].should != "ab"
        pass
    
    assert spec.run(success_spec).wasSuccessful()
    assert len(spec.run(fail_spec).failures) == 2
    pass

@spec_for_expect.that("for instance")
def behavior(its):
    from specfor import the
    
    success_spec = spec.of("instance")
    @success_spec.that("the[val].should.be_instance_of[exp_type]")
    def behavior(it):
        the[{}].should.be_instance_of[dict]
        pass
    
    fail_spec = spec.of("instance")
    @fail_spec.that("the[val].should.be_instance_of[exp_type]")
    def behavior(it):
        the[{}].should.be_instance_of[list]
        pass
    
    assert spec.run(success_spec).wasSuccessful()
    assert not spec.run(fail_spec).wasSuccessful()
    pass

spec.publish(globals())
