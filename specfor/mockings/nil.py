
class NilClass(object):
    def __repr__(self):
        return "nil"
    
    def __len__(self):
        return 0
    def __iter__(self):
        return;yield
    
    def __cmp__(self, other):
        return cmp(None, other)
    __lt__ = __le__ = lambda self, other: True
    __gt__ = __ge__ = lambda self, other: False
    
    # cast
    __nonzero__ = __bool__ = lambda self: False
    __int__ = lambda self: 0
    __long__ = lambda self: long(0)
    __float__ = lambda self: float(0)
    __complex__ = lambda self: complex(0)
    __oct__ = lambda self: oct(0)
    __hex__ = lambda self: hex(0)
    
    # arith
    __divmod__ = __rdivmod__ = __coerce__ = lambda self, other: (nil, nil)
    
    __call__ = \
        __delattr__ = __getattr__ = __setattr__ = \
        __delitem__ = __getitem__ = __setitem__ = \
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
