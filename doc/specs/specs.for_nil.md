# specs.for_nil

## nil

### [nil] ignore any sideeffects

<pre>
@nil_spec.that("ignore any sideeffects")
def behavior(its):
    from specfor import mock
    nil = mock.nil
    
    nil["abc"] = 1000
    nil.abd = "def"
    del nil.foobar
    del nil["anc"]
    pass
</pre>

### [nil] as empty sequence

<pre>
@nil_spec.that("as empty sequence")
def behavior(its):
    from specfor import mock
    nil = mock.nil
    
    the[len(nil)].should.be[0]
    the[list(nil)].should.be[[]]
    the["abc" in nil].should.be_false
    pass
</pre>

### [nil] compare is same as None

<pre>
@nil_spec.that("compare is same as None")
def behavior(its):
    from specfor import mock
    nil = mock.nil
     
    the[nil < 10].should.be_true
    the[nil > 10].should.be_false
    pass
</pre>

### [nil] nil is not None

<pre>
@nil_spec.that("nil is not None")
def behavior(its):
    from specfor import mock
    nil = mock.nil
     
    the[nil != None].should.be_true
    the[nil == None].should.be_false
    the[nil is None].should.be_false
    pass
</pre>

### [nil] any access returns nil

<pre>
@nil_spec.that("any access returns nil")
def behavior(its):
    from specfor import mock
    nil = mock.nil
     
    the[nil.abc].should.be[nil]
    the[nil[1:2]].should.be[nil]
    the[nil(10, "abc")].should.be[nil]
    pass
</pre>

### [nil] arith ops returns nil

<pre>
@nil_spec.that("arith ops returns nil")
def behavior(its):
    from specfor import mock
    nil = mock.nil
     
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
    pass
</pre>

### [nil] bit ops returns nil

<pre>
@nil_spec.that("bit ops returns nil")
def behavior(its):
    from specfor import mock
    nil = mock.nil
     
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
    pass
</pre>

### [nil] unary ops returns nil

<pre>
@nil_spec.that("unary ops returns nil")
def behavior(its):
    from specfor import mock
    nil = mock.nil
    
    the[~nil].should.be[nil]
    the[-nil].should.be[nil]
    the[+nil].should.be[nil]
    pass
</pre>



