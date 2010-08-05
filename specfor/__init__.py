version = "0.0.1"
from .framework import *
from .expectation import *
from .mockings import *

def refresh():
    """refresh specfor module. returned module is cleanup all extra plugins
    
    usage:
    
        global specfor
        specfor = specfor.refresh()
    """
    import sys
    names = [k for k in sys.modules if k.startswith("specfor")]
    for name in names:
        del sys.modules[name]
        pass
    return __import__("specfor")

__all__ = ["the", "spec", "mock"]
