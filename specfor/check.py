"""simple spec file checker: python -m specfro.check specdir/*.py
"""
from __future__ import with_statement
import imp
import os
import sys
import unittest

class SpecRunner(object):
    def __init__(self, runner=None, loader=None):
        self.runner = runner or unittest.TextTestRunner()
        self.loader = loader or unittest.TestLoader()
        pass
    
    def run(self, files):
        sysmods = sys.modules.copy()
        try:
            mods = self.load_mods(files)
            result = self.invoke_runner(mods)
            return result
        finally:
            sys.modules = sysmods
            pass
        pass
    
    def load_mods(self, files):
        mods = []
        for filename in files:
            modname = self.f2m(filename)
            if not modname: continue
            with open(filename) as f:
                code = compile(f.read(), filename, "exec")
                mod = self.exec_code(code, modname)
                sys.modules[modname] = mod
                mods.append(mod)
                pass
            pass
        return mods
    
    def invoke_runner(self, mods):
        suite = unittest.TestSuite()
        for mod in mods:
            test = self.loader.loadTestsFromModule(mod)
            suite.addTest(test)
            pass
        return self.runner.run(suite)
    
    def f2m(self, filename):
        names = os.path.normpath(filename).split(os.path.sep)
        name, ext = os.path.splitext(names[-1])
        if ext != ".py": return None
        if name == "__init__": return ".".join(names[:-1])
        return ".".join(names[:-1] + [name])
    
    def exec_code(self, code, name):
        mod = imp.new_module(name)
        exec(code, mod.__dict__)
        return mod

    pass

def main():
    import optparse
    parser = optparse.OptionParser(
        usage="%prog [opts] files ...",
        description="run spec as unittest")
    parser.add_option(
        "-q", "--quite", action="store_const", const=0, dest="verbosity", 
        default=1)
    parser.add_option(
        "-v", "--verbose", action="store_const", const=2, dest="verbosity", 
        default=1)
    
    opts, files = parser.parse_args()
    runner = unittest.TextTestRunner(verbosity=opts.verbosity)
    result = SpecRunner(runner).run(files)
    if not result.wasSuccessful(): sys.exit(1)
    pass

if __name__ == "__main__": main()
