from . import plugins

class SimpleMarkdown(plugins.DocumentGenerator):
    def __init__(self, opts):
        pass
    def convert(self, module):
        for line in self.convert_module(module):
            yield line
            pass
        pass
    
    def convert_module(self, module):
        yield "# %s\n\n" % module.name
        for spec in module.specs:
            for _ in self.convert_spec(spec): yield _
            pass
        yield "\n"
        return
    
    def convert_spec(self, spec):
        yield "## %s\n\n" % spec.name
        for behavior in spec.behaviors:
            for _ in self.convert_behavior(spec, behavior): yield _
            pass
        for bbehavior in spec.bundle_behaviors:
            for _ in self.convert_bundle_behavior(spec, bbehavior): yield _
            pass
        yield "\n"
        return
    
    def convert_behavior(self, spec, behavior):
        yield "### [%s] %s\n\n" % (spec.name, behavior.description)
        for prepare in spec.prepares:
            for _ in self.convert_func(prepare): yield _
            pass
        for _ in self.convert_func(behavior.definition): yield _
        for cleanup in spec.cleanups:
            for _ in self.convert_func(cleanup): yield _
            pass
        yield "\n"
        return
    
    def convert_bundle_behavior(self, spec, bundle_behavior):
        behavior = bundle_behavior.behavior
        bundle = bundle_behavior.bundle
        setup = bundle_behavior.setup
        yield "### [%s] %s: %s\n\n" % (
            spec.name, bundle.name, behavior.description)
        for prepare in spec.prepares:
            for _ in self.convert_func(prepare): yield _
            pass
        if setup: 
            for _ in self.convert_func(setup): yield _
            pass
        for prepare in bundle.prepares:
            for _ in self.convert_func(prepare): yield _
            pass
        for _ in self.convert_func(behavior.definition): yield _
        for cleanup in bundle.cleanups:
            for _ in self.convert_func(cleanup): yield _
            pass
        for cleanup in spec.cleanups:
            for _ in self.convert_func(cleanup): yield _
            pass
        yield "\n"
        return
    
    def convert_func(self, func):
        yield "<pre>\n"
        yield func.source
        yield "</pre>\n"
        return
    
    pass
plugins.register("simple", SimpleMarkdown)
