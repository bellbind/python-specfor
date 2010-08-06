from .. import plugins

class OrderedRestriction(plugins.Restriction):
    name = "ordered"
    def __init__(self, context):
        self.context = context
        self.passed = False
        pass
    def called(self, responsibilities, returns, args, kwargs):
        target = args[0]
        check = (not hasattr(target, "_ordered") or 
                 target._ordered + 1 == self.context)
        assert check, ("called invalid order: %s" % repr(responsibilities))
        target._ordered = self.context
        self.passed = True
        return True
    def completed(self, responsibilities):
        assert self.passed, "not passed yet: %s" % repr(responsibilities)
        pass
    def __repr__(self):
        return "[%s passed]" % ("already" if self.passed else "yet")

    pass
plugins.register(
    "ordered", lambda resp, context: OrderedRestriction(context))
