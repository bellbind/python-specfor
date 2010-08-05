from specfor import the, spec

mock_spec = spec.of("nil")
@mock_spec.that("nil accepts any method with no effect")
def behavior(its):
    from specfor import mock
    nil = mock.nil
    
    # ignore any sideeffects
    nil["abc"] = 1000
    nil.abd = "def"
    del nil.foobar
    del nil["anc"]

    # as empty sequence 
    the[len(nil)].should.be[0]
    the[list(nil)].should.be[[]]
    the["abc" in nil].should.be_false

    # compare is same as None
    the[nil < 10].should.be_true
    the[nil > 10].should.be_false
    # nil is not None
    the[nil != None].should.be_true
    the[nil == None].should.be_false
    the[nil is None].should.be_false
    
    # any access returns nil
    the[nil.abc].should.be[nil]
    the[nil[1:2]].should.be[nil]
    the[nil(10, "abc")].should.be[nil]
    
    # arith ops returns nil
    the[nil + 10].should.be[nil]
    the[10 + nil].should.be[nil]
    the[nil - 10].should.be[nil]
    the[10 - nil].should.be[nil]
    the[nil * 10].should.be[nil]
    the[10 * nil].should.be[nil]
    the[10 // nil].should.be[nil]
    the[nil // 10].should.be[nil]
    the[10 / nil].should.be[nil]
    the[nil / 10].should.be[nil]
    the[10 % nil].should.be[nil]
    the[nil % 10].should.be[nil]
    the[10 ** nil].should.be[nil]
    the[nil ** 10].should.be[nil]
    
    the[10 & nil].should.be[nil]
    the[nil & 10].should.be[nil]
    the[10 | nil].should.be[nil]
    the[nil | 10].should.be[nil]
    the[10 ^ nil].should.be[nil]
    the[nil ^ 10].should.be[nil]
    the[10 << nil].should.be[nil]
    the[nil << 10].should.be[nil]
    the[10 >> nil].should.be[nil]
    the[nil >> 10].should.be[nil]

    the[~nil].should.be[nil]
    the[-nil].should.be[nil]
    the[+nil].should.be[nil]
    pass

spec.publish(globals())
