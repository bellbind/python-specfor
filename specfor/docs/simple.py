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
        header = "# %s\n\n" % module.name
        lines = []
        for spec in module.specs:
            lines.extend(self.convert_spec(spec))
            pass
        return [header] + lines + ["\n"]
    
    def convert_spec(self, spec):
        header = "## %s\n\n" % spec.name
        lines = []
        for behavior in spec.behaviors:
            lines.extend(self.convert_behavior(spec, behavior))
            pass
        for bundle_behavior in spec.bundle_behaviors:
            ls = self.convert_bundle_behavior(spec, bundle_behavior)
            lines.extend(ls)
            pass
        return [header] + lines + ["\n"]
    
    def convert_behavior(self, spec, behavior):
        header = "### [%s] %s\n\n" % (spec.name, behavior.description)
        lines = []
        for prepare in spec.prepares:
            lines.extend(self.convert_func(prepare))
            pass
        lines.extend(self.convert_func(behavior.definition))
        for cleanup in spec.cleanups:
            lines.extend(self.convert_func(cleanup))
            pass
        return [header] + lines + ["\n"]
    
    def convert_bundle_behavior(self, spec, bundle_behavior):
        behavior = bundle_behavior.behavior
        bundle = bundle_behavior.bundle
        setup = bundle_behavior.setup
        header = "### [%s] %s: %s\n\n" % (
            spec.name, bundle.name, behavior.description)
        lines = []
        for prepare in spec.prepares:
            lines.extend(self.convert_func(prepare))
            pass
        if setup: lines.extend(self.convert_func(setup))
        for prepare in bundle.prepares:
            lines.extend(self.convert_func(prepare))
            pass
        lines.extend(self.convert_func(behavior.definition))
        for cleanup in bundle.cleanups:
            lines.extend(self.convert_func(cleanup))
            pass
        for cleanup in spec.cleanups:
            lines.extend(self.convert_func(cleanup))
            pass
        return [header] + lines + ["\n"]
    
    def convert_func(self, func):
        return ["<pre>\n", func.source, "</pre>\n"]
    
    pass
plugins.register("simple", SimpleMarkdown)
