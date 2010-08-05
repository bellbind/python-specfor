from .. import walker

class DocumentGenerator(object):
    def __init__(self, opts):
        self.opts = opts
        pass
    def convert(self, module):
        yield ""
        pass
    pass

doc_generators = {}

def register(name, doc_generator):
    doc_generators[name] = doc_generator
    pass

def convert(name, opts, module):
    doc_generator = doc_generators.get(name)(opts)
    for line in doc_generator.convert(walker.ModuleNode(module)):
        yield line
        pass
    pass


