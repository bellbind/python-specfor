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
    @fail_spec.that("with the.raising[exception]: raise_invalid_error()")
    def behavior(it):
        with the.raising[KeyError]:
            []["abc"]
            pass
        pass
    
    
    assert spec.run(success_spec).wasSuccessful()
    assert len(spec.run(fail_spec).failures) == 2
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

@spec_for_expect.that("for true value")
def behavior(its):
    from specfor import the
    
    success_spec = spec.of("be true")
    @success_spec.that("the[val].should.be_true")
    def behavior(it):
        the[True].should.be_true
        pass
    @success_spec.that("the[val].should.be_ok")
    def behavior(it):
        the[10].should.be_ok
        pass
    
    fail_spec = spec.of("be true")
    @fail_spec.that("the[val].should.be_true")
    def behavior(it):
        the[0].should.be_true
        pass
    @fail_spec.that("the[val].should.be_ok")
    def behavior(it):
        the[{}].should.be_ok
        pass
    
    assert spec.run(success_spec).wasSuccessful()
    assert len(spec.run(fail_spec).failures) == 2
    pass

@spec_for_expect.that("for false value")
def behavior(its):
    from specfor import the
    
    success_spec = spec.of("be false")
    @success_spec.that("the[val].should.be_false")
    def behavior(it):
        the[False].should.be_false
        pass
    @success_spec.that("the[val].should.be_no")
    def behavior(it):
        the[{}].should.be_no
        pass
    
    fail_spec = spec.of("be false")
    @fail_spec.that("the[val].should.be_false")
    def behavior(it):
        the["abc"].should.be_false
        pass
    @fail_spec.that("the[val].should.be_ok")
    def behavior(it):
        the[ValueError].should.be_no
        pass
    
    assert spec.run(success_spec).wasSuccessful()
    assert len(spec.run(fail_spec).failures) == 2
    pass


@spec_for_expect.that("for existence")
def behavior(its):
    from specfor import the
    
    success_spec = spec.of("exist")
    @success_spec.that("the[val].should.exist")
    def behavior(it):
        the[{}].should.exist
        pass
    
    fail_spec = spec.of("exist")
    @fail_spec.that("the[val].should.exist")
    def behavior(it):
        the[None].should.exist
        pass
    assert spec.run(success_spec).wasSuccessful()
    assert not spec.run(fail_spec).wasSuccessful()
    pass

@spec_for_expect.that("for none existence")
def behavior(its):
    from specfor import the
    
    success_spec = spec.of("not_exist")
    @success_spec.that("the[val].should.not_exist")
    def behavior(it):
        the[None].should.not_exist
        pass
    
    fail_spec = spec.of("not_exist")
    @fail_spec.that("the[val].should.not_exist")
    def behavior(it):
        the[{}].should.not_exist
        pass
    assert spec.run(success_spec).wasSuccessful()
    assert not spec.run(fail_spec).wasSuccessful()
    pass

@spec_for_expect.that("for member of collection")
def behavior(its):
    from specfor import the
    
    success_spec = spec.of("be_in")
    @success_spec.that("the[val].should.be_in[collection]")
    def behavior(it):
        the["abc"].should.be_in[["abc", "def"]]
        pass
    
    fail_spec = spec.of("be_in")
    @fail_spec.that("the[val].should.be_in[collection]")
    def behavior(it):
        the["abc"].should.be_in[set(["abd", "def"])]
        pass
    assert spec.run(success_spec).wasSuccessful()
    assert not spec.run(fail_spec).wasSuccessful()
    pass

@spec_for_expect.that("for none member of collection")
def behavior(its):
    from specfor import the
    
    success_spec = spec.of("not_be_in")
    @success_spec.that("the[val].should.not_be_in[collection]")
    def behavior(it):
        the["abd"].should.not_be_in[["abc", "def"]]
        pass
    
    fail_spec = spec.of("not_be_in")
    @fail_spec.that("the[val].should.not_be_in[collection]")
    def behavior(it):
        the["abc"].should.not_be_in[set(["abc", "def"])]
        pass
    assert spec.run(success_spec).wasSuccessful()
    assert not spec.run(fail_spec).wasSuccessful()
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


@spec_for_expect.that("for inordered collection")
def behavior(its):
    from specfor import the
    
    success_spec = spec.of("be_same_as")
    @success_spec.that("the[val].should.be_same_as[collection]")
    def behavior(it):
        the[["def", "abc"]].should.be_same_as[["abc", "def"]]
        pass
    
    fail_spec = spec.of("be_same_as")
    @fail_spec.that("the[val].should.be_same_as[collection]")
    def behavior(it):
        the[["def", "abc", "ghi"]].should.be_same_as[["abc", "def"]]
        pass
    assert spec.run(success_spec).wasSuccessful()    
    assert not spec.run(fail_spec).wasSuccessful()
    pass

@spec_for_expect.that("for ordered collection")
def behavior(its):
    from specfor import the
    
    success_spec = spec.of("be_same_order_as")
    @success_spec.that("the[val].should.be_same_order_as[collection]")
    def behavior(it):
        the[["abc", "def"]].should.be_same_order_as[["abc", "def"]]
        pass
    
    fail_spec = spec.of("be_same_order_as")
    @fail_spec.that("the[val].should.be_same_order_as[collection]")
    def behavior(it):
        the[["def", "abc"]].should.be_same_order_as[["abc", "def"]]
        pass
    assert spec.run(success_spec).wasSuccessful()    
    assert not spec.run(fail_spec).wasSuccessful()
    pass



spec.publish(globals())
