from specfor import spec


spec_for_spec = spec.of("spec for specfor.spec")
@spec_for_spec.that("successful behavior")
def behavior(its):
    log = []
    a_spec = spec.of("a spec")
    @a_spec.that("check done")
    def behavior(it):
        log.append("done")
        pass
    
    test, r = run_as_test(a_spec)
    assert log[0] == "done"
    assert r.wasSuccessful()
    pass


@spec_for_spec.that("failure behavior")
def behavior(its):
    a_spec = spec.of("a spec")
    @a_spec.that("raise AssertionError")
    def behavior(it):
        assert False, "error"
        pass
    
    # check as unittest.TestCase
    test, r = run_as_test(a_spec)
    assert not r.wasSuccessful()
    pass


@spec_for_spec.that("with before processing")
def behavior(its):
    log = []
    a_spec = spec.of("a spec")
    @a_spec.that("check done")
    def behavior(it):
        log.append("behavior")
        pass
    @a_spec.before()
    def prepare(it):
        log.append("prepare")
        pass
    
    # check as unittest.TestCase
    test, r = run_as_test(a_spec)
    assert len(log) == 2
    assert log[0] == "prepare"
    assert log[1] == "behavior"
    pass


@spec_for_spec.that("with after processing")
def behavior(its):
    log = []
    a_spec = spec.of("a spec")
    @a_spec.that("check done")
    def behavior(it):
        log.append("behavior")
        pass
    @a_spec.after()
    def cleanup(it):
        log.append("after")
        pass
    
    # check as unittest.TestCase
    test, r = run_as_test(a_spec)
    assert len(log) == 2
    assert log[0] == "behavior"
    assert log[1] == "after"
    pass

@spec_for_spec.that("failure behavior with after processing: after could run")
def behavior(its):
    log = []
    a_spec = spec.of("a spec")
    @a_spec.that("check done")
    def behavior(it):
        assert False
        log.append("behavior")
        pass
    @a_spec.after()
    def cleanup(it):
        log.append("after")
        pass
    
    # check as unittest.TestCase
    test, r = run_as_test(a_spec)
    assert len(log) == 1
    assert log[0] == "after"
    pass


@spec_for_spec.that("with multiple before-afters: run with defined order")
def behavior(its):
    log = []
    a_spec = spec.of("a spec")
    @a_spec.that("check done")
    def behavior(it):
        log.append("behavior")
        pass
    @a_spec.before()
    def prepare1(it):
        log.append("before1")
        pass
    @a_spec.before()
    def prepare2(it):
        log.append("before2")
        pass
    @a_spec.after()
    def cleanup1(it):
        log.append("after1")
        pass
    @a_spec.after()
    def cleanup2(it):
        log.append("after2")
        pass
    
    # check as unittest.TestCase
    test, r = run_as_test(a_spec)
    assert len(log) == 5
    assert log[0] == "before1"
    assert log[1] == "before2"
    assert log[2] == "behavior"
    assert log[3] == "after1"
    assert log[4] == "after2"
    pass


@spec_for_spec.that("share a behavior by multiple specs")
def behavior(its):
    a_spec = spec.of("spec A")
    b_spec = spec.of("spec B")
    @a_spec.before()
    def prepare(it): it.name = "A"
    @b_spec.before()
    def prepare(it): it.name = "B"
    
    @a_spec.that("check done for A")
    @b_spec.that("check done for B")
    def behavior(it):
        it.value = "done " + it.name
        pass
    
    # check as unittest.TestCase
    a_test, r = run_as_test(a_spec)
    b_test, r = run_as_test(b_spec)
    assert a_test.value == "done A"
    assert b_test.value == "done B"
    pass


@spec_for_spec.that("use behavior bundle")
def behavior(its):
    bundle = spec.behaviors_of("behaviors bundle")
    @bundle.that("a behavior")
    def behavior(it):
        it.value = it.name + " done"
        pass
    
    a_spec = spec.of("a spec")
    @a_spec.of(bundle)
    def glue(it):
        it.name = "a spec"
        pass
    
    test, r = run_as_test(a_spec)
    assert test.value == "a spec done"
    pass


@spec_for_spec.that("use behavior bundle with before-after")
def behavior(its):
    log = []
    bundle = spec.behaviors_of("behaviors bundle")
    @bundle.that("a behavior")
    def behavior(it):
        log.append("behavior")
        pass
    @bundle.before()
    def prepare(it):
        log.append("bundle before")
        pass
    @bundle.after()
    def cleanup(it):
        log.append("bundle after")
        pass
    
    a_spec = spec.of("a spec")
    @a_spec.before()
    def prepare_spec(it):
        log.append("spec before")
        pass
    @a_spec.after()
    def cleanup_spec(it):
        log.append("spec after")
        pass
    @a_spec.of(bundle)
    def glue(it):
        log.append("glue")
        pass
    
    test, r = run_as_test(a_spec)
    assert len(log) == 6
    assert log[0] == "spec before"
    assert log[1] == "glue"
    assert log[2] == "bundle before"
    assert log[3] == "behavior"
    assert log[4] == "bundle after"
    assert log[5] == "spec after"
    pass


def run_as_test(spec, r=None):
    import unittest
    r = r or unittest.TestResult()
    names = [n for n in dir(spec) if n.startswith("test")]
    assert len(names) == 1
    test = spec(names[0])
    test.run(r)
    return test, r

spec.publish(globals())
