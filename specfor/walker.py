import inspect
from .framework import Spec

class ModuleNode(object):
    def __init__(self, module):
        self.module = module
        pass
    
    @property
    def specs(self):
        for name in dir(self.module):
            obj = getattr(self.module, name)
            if isinstance(obj, type) and issubclass(obj, Spec):
                yield SpecNode(obj)
                pass
            pass
        pass
    
    @property
    def name(self):
        return self.module.__name__
    pass

class BundleNode(object):
    def __init__(self, bundle):
        self.bundle = bundle
        pass
    
    @property
    def behaviors(self):
        if not self.bundle.behaviors: return
        for name in self.bundle.behaviors:
            behavior = getattr(self.bundle, name)
            yield BehaviorNode(behavior)
            pass
        pass
    @property
    def prepares(self):
        if not self.bundle.prepares: return
        for prepare in self.bundle.prepares:
            yield FunctionNode(prepare)
            pass
        pass
    @property
    def cleanups(self):
        if not self.bundle.cleanups: return
        for cleanup in self.bundle.cleanups:
            yield FunctionNode(cleanup)
            pass
        pass
    @property
    def name(self):
        return self.bundle.__name__
    pass

class SpecNode(BundleNode):
    @property
    def bundles(self):
        if not self.bundle.bundles: return
        for bundle in self.bundle.bundles:
            yield BundleNode(bundle)
            pass
        pass
    @property
    def bundle_behaviors(self):
        if not self.bundle.bundlebehaviors: return
        for bundlebehavior in self.bundle.bundlebehaviors:
            yield BundleBahaviorNode(bundlebehavior)
            pass
        pass
    pass

class BundleBahaviorNode(object):
    def __init__(self, bundlebehavior):
        self.bundlebehavior = bundlebehavior
        pass
    @property
    def behavior(self):
        return BehaviorNode(self.bundlebehavior.behavior)
    @property
    def bundle(self):
        return BundleNode(self.bundlebehavior.bundle)
    @property
    def setup(self):
        return FunctionNode(self.bundlebehavior.setup)
    pass

class BehaviorNode(object):
    def __init__(self, behavior):
        self.behavior = behavior
        pass
    @property
    def definition(self):
        return FunctionNode(self.behavior.definition)
    @property
    def description(self):
        return self.behavior.description
    pass

class FunctionNode(object):
    def __init__(self, func):
        self.func = func
        pass
    @property
    def name(self):
        return self.func.__name__
    @property
    def source(self):
        return inspect.getsource(self.func)
    pass

