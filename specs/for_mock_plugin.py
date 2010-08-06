from __future__ import with_statement
from specfor import spec, the

spec_mock_plugin = spec.of("mock plugin")
@spec_mock_plugin.that("add new restriction")
def behavior(its):
    import specfor
    new_specfor = specfor.new_specfor()
    mock = new_specfor.mock
    plugins = new_specfor.mockings.plugins
    
    # new restriction
    class NeverRestriction(plugins.Restriction):
        name = "never"
        def prepare(self, responsibilities, *args, **kwargs):
            return True
        def called(self, responsibilities, returns, *args, **kwargs):
            return False # fail if called
        def completed(self, responsibilities):
            return
        def __repr__(self):
            return "[never]"
        pass
    plugins.register("never", lambda resp, val: NeverRestriction())
    
    # mock
    person_mock = mock.define("person")
    prop_def = person_mock.property("age")
    @prop_def.get.always
    def age(self):
        return 18
    @prop_def.set.define(never=True, like=dict(val=str))
    def age(self, val):
        return
    @prop_def.set.always
    def age(self, val):
        return
    
    
    # use
    person = person_mock("id-0")
    
    the[person.age].should.be[18]
    person.age = 20
    the[person.age].should.be[18]
    with the.raising[AssertionError]:
        person.age = "20"
        pass
    pass

@spec_mock_plugin.after()
def check_clean_env(its):
    from specfor.mockings.plugins import plugins
    the["never"].should.not_be_in[dir(plugins)]
    pass

spec.publish(globals())
