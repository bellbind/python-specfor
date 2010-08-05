version = "0.0.5"
from .framework import *
from .expectation import *
from .mockings import *

def new_specfor():
    import sys
    names = [k for k in sys.modules if k.startswith("specfor")]
    origs = {}
    for name in names:
        origs[name] = sys.modules[name]
        del sys.modules[name]
        pass
    new = __import__("specfor")
    sys.modules.update(origs)
    return new

__all__ = ["the", "spec", "mock"]
