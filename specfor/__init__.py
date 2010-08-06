version = "0.1.0"

from .framework import spec
from .expectation import the
from .mockings import mock

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
