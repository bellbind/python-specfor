import inspect
import itertools
import re
from . import plugins

class ArgsRestiction(plugins.Restriction):
    name = "args"
    def __init__(self, argspec):
        self.argspec = argspec
        pass
    def prepare(self, responsibilities, args, kwargs):
        return self.argspec.accept(args, kwargs)
    def called(self, responsibilities, returns, args, kwargs):
        return True
    def completed(self, responsibilities):
        return
    def __repr__(self):
        return "(%s)" % (repr(self.argspec))
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

# plugin

def just_factory(resp, kwargs):
    kwspecs = dict((k, ArgSpecJust(k, v)) for k, v in kwargs.items())
    funcspec = inspect.getargspec(resp.result)
    argspec = ArgSpecs(kwspecs, funcspec)
    return ArgsRestiction(argspec)
plugins.register("just", just_factory)

def like_factory(resp, kwargs):
    kwspecs = dict((k, ArgSpecLike(k, v)) for k, v in kwargs.items())
    funcspec = inspect.getargspec(resp.result)
    argspec = ArgSpecs(kwspecs, funcspec)
    return ArgsRestiction(argspec)
plugins.register("like", like_factory)

def unless_factory(resp, kwargs):
    kwspecs = dict((k, ArgSpecNot(k, v)) for k, v in kwargs.items())
    funcspec = inspect.getargspec(resp.result)
    argspec = ArgSpecs(kwspecs, funcspec)
    return ArgsRestiction(argspec)
plugins.register("unless", unless_factory)

