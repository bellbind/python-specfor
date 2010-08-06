from specfor import the, spec

mock_spec = spec.of("mock")
@mock_spec.that("define mock and create instance and chek")
def behavior(its):
    from specfor import mock
    
    empty_mock = mock.define("empty")
    empty = empty_mock("id-0")
    mock.check(empty)
    pass

@mock_spec.that("define method")
def behavior(its):
    from specfor import mock
    
    converter_mock = mock.define("converter")
    method = converter_mock.method("convert")
    @method.define(just=dict(item=0))
    def convert(self, item):
        return "zero"
    @method.define(just=dict(item=1))
    def convert(self, item):
        return "one"
    @method.define(like=dict(item=int))
    def convert(self, item):
        return "many"
    
    converter = converter_mock("id-0")
    
    the[converter.convert(0)].should.be["zero"]
    the[converter.convert(1)].should.be["one"]
    the[converter.convert(10)].should.be["many"]
    
    pass

@mock_spec.that("define property")
def behavior(its):
    from specfor import mock
    log = []
    
    consts_mock = mock.define("consts")
    prop = consts_mock.property("content_type")
    @prop.get.always
    def content_type(self):
        log.append("get")
        return "text/html"
    @prop.set.always
    def content_type(self, val):
        log.append("ignored")
        return
    
    consts = consts_mock("id-0")
    
    the[consts.content_type].should.be["text/html"]
    consts.content_type = "application/xml"
    the[consts.content_type].should.be["text/html"]
    
    the[log].should.be_same_order_as[["get", "ignored", "get"]]
    pass

@mock_spec.that("raise AttributeError if access undefined attr")
def behavior(its):
    from specfor import mock
    
    empty_mock = mock.define("empty")
    empty = empty_mock("id-0")
    
    with the.raising[AttributeError]:
        empty.foobar
        pass
    pass


spec.publish(globals())
