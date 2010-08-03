import itertools
from . import plugins

# mock

class Mock(object):
    def __init__(self, mockid=None):
        self._mockid = mockid or ("%x" % id(self))
        pass
    def __repr__(self):
        return "<%s:%s>" % (self.__class__.__name__, self._mockid)
    pass

class MockMethod(object):
    def __init__(self, name):
        self.name = name
        self.responsibilities = []
        pass
    def __call__(self, *args, **kwargs):
        for responsibility in self.responsibilities:
            if responsibility.responds(*args, **kwargs):
                return responsibility.returns(*args, **kwargs)
            pass
        assert False, "There is no responsibility: %s" % (
            self.reprmethod(args, kwargs))
        raise RuntimeError
    def reprmethod(self, args, kwargs):
        reprargs = ", ".join(
            itertools.chain(
                (repr(arg) for arg in args),
                ("%s=%s" % (k, repr(v)) for k, v in kwargs.items())))
        return "%s(%s)" % (self.name, reprargs)
    def __repr__(self):
        return "%s" % (self.name)
    def to_func(self):
        def func(*args, **kwargs):
            return self(*args, **kwargs)
        func.mock = self
        return func
    def check_complete(self):
        for resp in self.responsibilities:
            resp.check_complete()
            pass
        pass
    pass

class Responsibility(object):
    def __init__(self, method, result):
        self.method = method
        self.result = result
        self.restrictions = []
        method.responsibilities.append(self)
        pass
    def responds(self, *args, **kwargs):
        for restrictions in self.restrictions:
            if not restrictions.prepare(self, args, kwargs): return False
            pass
        return True
    def returns(self, *args, **kwargs):
        ret = self.result(*args, **kwargs)
        for restrictions in self.restrictions:
            if not restrictions.called(self, ret, args, kwargs): return False
            pass
        return ret
    def check_complete(self):
        for restrictions in self.restrictions:
            restrictions.completed(self)
            pass
        return
    def __repr__(self):
        return repr(self.method) + "".join(
            repr(rest) for rest in self.restrictions)
    pass

# checker
class MockChecker(object):
    proptype = type(property())
    def __call__(self, mock):
        members = mock.__class__._mock_members
        for name, member in members.items():
            self.check_member(member)
            pass
        return True
    def check_member(self, member):
        if type(member) == self.proptype:
            return self.check_property(member)
        else:
            return self.check_method(member)
        pass
    def check_property(self, prop):
        if prop.fget: self.check_method(prop.fget)
        if prop.fset: self.check_method(prop.fget)
        return
    def check_method(self, method):
        return method.mock.check_complete()
    pass


# DSL
class MockDef(object):
    def __init__(self, name):
        self.name = name
        self.methods = {}
        self.properties = {}
        pass
    def method(self, name):
        if name not in self.methods: 
            self.methods[name] = MethodDef(name)
            pass
        return self.methods[name]
    def property(self, name):
        if name not in self.properties: 
            self.properties[name] = PropertyDef(name)
            pass
        return self.properties[name]
    def __call__(self, *args, **kwargs):
        return MockCreator().create_mocktype(self)(*args, **kwargs)
    pass


class MethodDef(object):
    def __init__(self, name):
        self.name = name
        self.respdefs = []
        pass
    def __call__(self, func):
        return self.always(func)
    def define(self, **kwargs):
        respdef = RespDef(kwargs)
        self.respdefs.append(respdef)
        return respdef
    @property
    def always(self):
        respdef = RespDef({})
        self.respdefs.append(respdef)
        return respdef
    pass

class PropertyDef(object):
    def __init__(self, name):
        self.name = name
        self.get = MethodDef(name)
        self.set = MethodDef(name)
        pass
    pass
    
class RespDef(object):
    def __init__(self, kwargs):
        self.kwargs = kwargs
        pass
    def __call__(self, func):
        self.result = func
        return func
    pass


class MockCreator(object):
    def create_mocktype(self, mockdef):
        members = {}
        for name, mdef in mockdef.methods.items():
            members[name] = self.create_mockmethod(mdef)
            pass
        for name, pdef in mockdef.properties.items():
            members[name] = self.create_property(pdef)
            pass
        mocktype = type(mockdef.name, (Mock,), members)
        mocktype._mock_members = members
        return mocktype
    
    def create_mockmethod(self, mdef):
        method = MockMethod(mdef.name)
        for respdef in mdef.respdefs:
            self.create_responsibility(method, respdef)
            pass
        return method.to_func()
    
    def create_responsibility(self, method, respdef):
        resp = Responsibility(method, respdef.result)
        rests = plugins.to_restrictions(resp, respdef.kwargs)
        resp.restrictions.extend(rests)
        return resp
    
    def create_property(self, pdef):
        getter = self.create_mockmethod(pdef.get)
        setter = self.create_mockmethod(pdef.set)
        prop = property(getter, setter)
        return prop
    pass

# API root
class MockEngine(object):
    def define(self, name):
        return MockDef(name)
    check = MockChecker()
    pass
