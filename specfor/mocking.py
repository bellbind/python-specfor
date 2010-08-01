import inspect
import itertools
import re
import types

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
    def __init__(self, method, argspecs, result, calls):
        self.method = method
        self.argspecs = argspecs
        self.result = result
        self.calls = calls
        self.count = 0
        method.responsibilities.append(self)
        pass
    def responds(self, *args, **kwargs):
        if self.finished(): return False
        return self.argspecs.accept(args, kwargs)
    def returns(self, *args, **kwargs):
        ret = self.result(*args, **kwargs)
        self.count += 1
        return ret
    def completed(self):
        return self.calls.completed(self.count)
    def finished(self):
        return self.calls.finished(self.count)
    def check_complete(self):
        if self.completed(): return
        assert False, "presonsibility not completed: %s" % repr(self)
    def __repr__(self):
        return "%s(%s)[%s|%s]" % (
            repr(self.method),
            repr(self.argspecs),
            self.count,
            repr(self.calls))
    pass


class ArgSpecs(object):
    def __init__(self, kwargspecs, funcspec):
        self.kwargspecs = kwargspecs
        self.funcspec = funcspec
        
        missings = []
        for argname in funcspec.args:
            if argname not in self.kwargspecs:
                missings.append(argname)
                pass
            pass
        if funcspec.varargs and funcspec.varargs not in self.kwargspecs:
            missings.append(funcspec.varargs)
            pass
        if funcspec.keywords and funcspec.keywords not in self.kwargspecs:
            missings.append(funcspec.keywords)
            pass
        for name in missings:
            self.kwargspecs[name] = ArgSpecAny(name)
            pass
        pass
    def __repr__(self):
        return ", ".join(itertools.chain(
                (repr(self.kwargspecs[n]) for n in self.funcspec.args),
                ["*" + repr(self.kwargspecs[self.funcspec.varargs])] 
                if self.funcspec.varargs else [],
                ["**" + repr(self.kwargspecs[self.funcspec.keywords])] 
                if self.funcspec.keywords else [],
                ))
    def accept(self, args, kwargs):
        arglen = len(self.funcspec.args)
        varargs = []
        keywords = {}
        consumes = []
        for i, arg in enumerate(args):
            if i >= arglen:
                varargs = args[i:]
                break
            argname = self.funcspec.args[i]
            if argname in self.kwargspecs:
                if not self.kwargspecs[argname].accept(arg): 
                    return False
                pass
            consumes.append(argname)
            pass
        
        for argname, value in kwargs.items():
            assert argname in consumes, (
                "[mock] dup in kwargs: %s" % argname)
            assert argname == self.funcspec.varargs, (
                "[mock] kwarg %s is varargs arg name" % argname)
            assert argname == self.funcspec.keywords, (
                "[mock] kwarg %s is keywords arg name" % argname)
            if argname in self.kwargspecs:
                if not self.kwargspecs[argname].accept(value):
                    return False
                consumes.append(argname)
                pass
            else:
                keywords[argname] = value
                pass
            pass
        if varargs:
            assert self.funcspec.varags, "[mock] too many args"
            if not self.kwargspecs[self.funcspec.varargs].accept(varargs):
                return False
            pass
        if keywords:
            assert self.funcspec.keywords, "[mock] too many kwargs"
            if not self.kwargspecs[self.funcspec.keywords].accept(keywords):
                return False
            pass
        return True
    pass

class CalledSpecAny(object):
    def __init__(self):
        pass
    def completed(self, count):
        return True
    def finished(self, count):
        return False
    def __repr__(self):
        return "*"
    pass

class CalledSpecJust(object):
    def __init__(self, count):
        self.count = count
        pass
    def completed(self, count):
        return self.count == count
    def finished(self, count):
        return self.count == count
    def __repr__(self):
        return "%s" % self.count
    pass

class CalledSpecUntil(object):
    def __init__(self, count):
        self.count = count
        pass
    def completed(self, count):
        return count <= self.count  
    def finished(self, count):
        return self.count == count
    def __repr__(self):
        return "<=%s" % self.count
    pass

class CalledSpecBetween(object):
    def __init__(self, mini, maxi):
        self.mini = mini
        self.maxi = maxi
        pass
    def completed(self, count):
        return self.mini <= count and count <= self.maxi
    def finished(self, count):
        return self.maxi == count
    def __repr__(self):
        return "%s..%s" % (self.mini, self.maxi)
    pass

class ArgSpecAny(object):
    def __init__(self, name):
        self.name = name
        pass
    def accept(self, arg):
        return True
    def __repr__(self):
        return self.name
    pass

class ArgSpecJust(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        pass
    def accept(self, arg):
        return self.value == arg
    def __repr__(self):
        return "%s=%s" % (self.name, repr(self.value))
    pass

class ArgSpecNot(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        pass
    def accept(self, arg):
        return self.value != arg
    def __repr__(self):
        return "%s!=%s" % (self.name, repr(self.value))
    pass

class ArgSpecLike(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        pass
    def accept(self, arg):
        vtype = type(self.value)
        if vtype == type:
            return isinstance(arg, self.value)
        if vtype == re._pattern_type:
            return self.value.match(arg) is not None
        if vtype == list or vtype == set or vtype == tuple:
            return arg in self.value
        if hasattr(self.value, "__call__"):
            return self.value(arg)
        return self.value == arg
    def __repr__(self):
        return "%s~=%s" % (self.name, repr(self.value))
    pass


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
    def just(self, **specs):
        kwspecs = dict((k, ArgSpecJust(k, v)) for k, v in specs.items())
        resp = RespDef(kwspecs)
        self.respdefs.append(resp)
        return resp
    def like(self, **specs):
        kwspecs = dict((k, ArgSpecLike(k, v)) for k, v in specs.items())
        resp = RespDef(kwspecs)
        self.respdefs.append(resp)
        return resp
    def unless(self, **specs):
        kwspecs = dict((k, ArgSpecNot(k, v)) for k, v in specs.items())
        resp = RespDef(kwspecs)
        self.respdefs.append(resp)
        return resp
    @property
    def always(self):
        resp = RespDef({})
        self.respdefs.append(resp)
        return resp
    pass

class PropertyDef(object):
    def __init__(self, name):
        self.name = name
        self.get = MethodDef(name)
        self.set = MethodDef(name)
        pass
    pass
    
class RespDef(object):
    def __init__(self, kwargspecs):
        self.kwargspecs = kwargspecs
        self.called = CalledSpecAny()
        pass
    def __call__(self, func):
        self.funcspec = inspect.getargspec(func)
        self.result = func
        return self
    pass

class CalledChanger(object):
    def at(self, count):
        def changer(respdef):
            respdef.called = CalledSpecJust(count)
            return respdef
        return changer
    def until(self, count):
        def changer(respdef):
            respdef.called = CalledSpecUntil(count)
            return respdef
        return changer
    def between(self, mini, maxi):
        def changer(respdef):
            respdef.called = CalledSpecBetween(mini, maxi)
            return respdef
        return changer
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
        argspecs = ArgSpecs(respdef.kwargspecs, respdef.funcspec)
        return Responsibility(method, argspecs, respdef.result, respdef.called)
    def create_property(self, pdef):
        getter = self.create_mockmethod(pdef.get)
        setter = self.create_mockmethod(pdef.set)
        prop = property(getter, setter)
        return prop
    pass


class MockEngine(object):
    def define(self, name):
        return MockDef(name)
    pass


mock = MockEngine()
mock.called = CalledChanger()
mock.check = MockChecker()
__all__ = ["mock"]
