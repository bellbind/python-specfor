
class NilClass(object):
    def __repr__(self):
        return "nil"
    
    # seq
    def __len__(self):
        return 0
    def __iter__(self):
        return;yield
    
    # compare
    def __eq__(self, other): return id(self) == id(other)
    def __ne__(self, other): return id(self) != id(other)
    def __cmp__(self, other): return cmp(None, other)
    def __lt__(self, other): return True
    def __le__ (self, other): return True
    def __gt__(self, other): return False
    def __ge__(self, other): return False
    
    # cast
    def __nonzero__(self): return False
    def __bool__(self): return False
    def __int__(self): return 0
    def __long__(self): return long(0)
    def __float__(self): return float(0)
    def __complex__(self): return complex(0)
    def __oct__(self): return oct(0)
    def __hex__(self): return hex(0)
    
    # access
    def __delattr__(self, k): return nil
    def __getattr__(self, k): return nil
    def __setattr__(self, k, v): return nil
    def __delitem__(self, k): return nil
    def __getitem__(self, k): return nil
    def __setitem__(self, k, v): return nil
    def __call__(self, *args, **kwargs): return nil

    # arith
    __divmod__ = __rdivmod__ = __coerce__ = lambda self, other: (nil, nil)
    __and__ = __or__ = __xor__ = __lshift__ = __rshift__ = \
        __add__ = __sub__ = __mul__ = \
        __div__ = __truediv__ = __floordiv__ = \
        __mod__ = __pow__ = \
        __rand__ = __ror__ = __rxor__ = __rlshift__ = __rrshift__ = \
        __radd__ = __rsub__ = __rmul__ = \
        __rdiv__ = __rtruediv__ = __rfloordiv__ = \
        __rmod__ = __rpow__ = \
        __neg__ = __pos__ = __abs__ = __invert__ = \
        __iand__ = __ior__ = __ixor__ = __ilshift__ = __irshift__ = \
        __iadd__ = __isub__ = __imul__ = \
        __idiv__ = __itruediv__ = __ifloordiv__ = \
        __imod__ = __ipow__ = \
        lambda self, *args, **kwargs: nil
    
    pass
nil = NilClass()
__all__ = ["nil"]
