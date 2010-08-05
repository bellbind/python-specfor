from . import plugins

class OrderedRestriction(plugins.Restriction):
    name = "ordered"
    def __init__(self, context):
        self.context = context
        self.passed = False
        order_list.append(self)
        pass
    def called(self, responsibilities, returns, args, kwargs):
        for rest in self.context:
            if rest == self: break
            assert rest.passed, (
                "called invalid order: %s" % repr(responsibilities))
            pass
        self.passed = True
        return True
    def completed(self, responsibilities):
        assert self.passed, "not passed yet: %s" % repr(responsibilities)
        pass
    def __repr__(self):
        return "[%s passed]" % ("already" if self.passed else "yet")

    pass
plugins.register(
    "ordered", lambda resp, context: OrderedRestiction(context))
