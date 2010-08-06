from specfor import the, spec

ordered_mock_spec = spec.of("mock with ordered call")
@ordered_mock_spec.that("define methods with ordered count")
def behavior(its):
    from specfor import mock
    
    callbacks_mock = mock.define("callbacks")
    method_def = callbacks_mock.method("init")
    @method_def.define(ordered=1) 
    def init(self):
        pass
    
    # next of ordered count should increment just 1
    method_def = callbacks_mock.method("prepare")
    @method_def.define(ordered=2) 
    def prepare(self):
        pass
    
    method_def = callbacks_mock.method("call")
    @method_def.define(ordered=3)
    def call(self):
        pass
    
    method_def = callbacks_mock.method("cleanup")
    @method_def.define(ordered=4)
    def cleanup(self):
        pass
    
    method_def = callbacks_mock.method("destroy")
    @method_def.define(ordered=5)
    def destroy(self):
        pass
    
    
    callbacks = callbacks_mock("id-0")
    # raise AssertionError if all ordered methods are not called
    with the.raising[AssertionError]: mock.check(callbacks)
    callbacks.init()
    callbacks.prepare()
    callbacks.call()
    # raise AssertionError if method called invalid order
    with the.raising[AssertionError]: callbacks.destroy()    
    callbacks.cleanup()
    callbacks.destroy()
    mock.check(callbacks)
    pass

spec.publish(globals())
