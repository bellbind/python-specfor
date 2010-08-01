import inspect
from .framework import Spec

class SimpleMarkdown(object):
    def convert_module(self, module):
        header = "# %s\n\n" % module.__name__
        lines = []
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, type) and issubclass(obj, Spec):
                lines.extend(self.convert_spec(obj))
                pass
            pass
        return [header] + lines + ["\n"]
    
    def convert_spec(self, spec_class):
        header = "## %s\n\n" % spec_class.__name__
        lines = []
        for name in spec_class.behaviors:
            behavior = getattr(spec_class, name)
            lines.extend(self.convert_behavior(spec_class, behavior))
            pass
        return [header] + lines + ["\n"]
    
    def convert_behavior(self, spec_class, behavior):
        header = "### [%s] %s\n\n" % (
            spec_class.__name__, behavior.description)
        lines = []
        for prepare in spec_class.prepares:
            lines.extend(self.convert_func(prepare))
            pass
        lines.extend(self.convert_func(behavior.definition))
        for cleanup in spec_class.cleanups:
            lines.extend(self.convert_func(cleanup))
            pass
        return [header] + lines + ["\n"]
    
    def convert_func(self, func):
        return ["<pre>\n", inspect.getsource(func), "</pre>\n"]
    
    def indent_count(self, line):
        count = 0
        for ch in line:
            if ch != " ": break 
            count += 1
            pass
        return count
    pass

def main():
    import optparse
    import os
    parser = optparse.OptionParser()
    opts, modnames = parser.parse_args()
    documenter = SimpleMarkdown()
    
    for modname in modnames:
        module = __import__(modname, fromlist=["*"])
        lines = documenter.convert_module(module)
        with open("%s%smd" % (modname, os.path.extsep), "w") as f:
            for line in lines:
                f.write(line)
                pass
            f.flush()
            pass
        pass
    pass

if __name__ == "__main__": main()
