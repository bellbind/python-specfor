from . import plugins

class CallRestiction(plugins.Restriction):
    name = "call"
    def __init__(self, callspec):
        self.callspec = callspec
        self.count = 0
        pass
    def prepare(self, responsibilities, args, kwargs):
        #return not self.callspec.finished(self.count)
        return True
    def called(self, responsibilities, returns, args, kwargs):
        self.count += 1
        return True
    def completed(self, responsibilities):
        assert self.callspec.completed(self.count), (
            "presonsibility not completed: %s" % repr(responsibilities))
        pass
    def __repr__(self):
        return "[%s|%s]" % (self.count, repr(self.callspec))
    pass

class CalledSpec(object):
    def __init__(self):
        pass
    def completed(self, count):
        return True
    def finished(self, count):
        return False
    def __repr__(self):
        return ""
    pass

class CalledSpecAny(CalledSpec):
    def __init__(self):
        pass
    def completed(self, count):
        return True
    def finished(self, count):
        return False
    def __repr__(self):
        return "*"
    pass
plugins.register("anytimes", lambda _: CallRestiction(CalledSpecAny()))

class CalledSpecJust(CalledSpec):
    def __init__(self, count):
        self.count = count
        pass
    def completed(self, count):
        return self.count == count
    def finished(self, count):
        return self.count == count
    def __repr__(self):
        return "==%s" % self.count
    pass
plugins.register(
    "at", lambda resp, count: CallRestiction(CalledSpecJust(count)))
plugins.register(
    "exactly", lambda resp, count: CallRestiction(CalledSpecJust(count)))

class CalledSpecUntil(CalledSpec):
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
plugins.register(
    "until", lambda resp, count: CallRestiction(CalledSpecUntil(count)))
plugins.register(
    "atmost", lambda resp, count: CallRestiction(CalledSpecUntil(count)))

class CalledSpecOver(CalledSpec):
    def __init__(self, count):
        self.count = count
        pass
    def completed(self, count):
        return self.count <= count
    def finished(self, count):
        return False
    def __repr__(self):
        return ">=%s" % self.count
    pass
plugins.register(
    "over", lambda resp, count: CallRestiction(CalledSpecOver(count)))
plugins.register(
    "atleast", lambda resp, count: CallRestiction(CalledSpecOver(count)))

class CalledSpecBetween(CalledSpec):
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
plugins.register(
    "between", 
    lambda resp, args: CallRestiction(CalledSpecBetween(args[0], args[1])))

    
    
    
