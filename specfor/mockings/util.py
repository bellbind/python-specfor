
def bindargs(funcspec, args, kwargs):
    """bind arg name and value by funcspec:
    
    - funcspec: result of inspect.getargspec(callable)
    - args: list of arg values
    - kwargs: dict of argnames and values
    - returns: None if args and funcspec are mismatch
    - returns: {argname: argvalue}
    """
    result = {}
    
    # bind args
    index = -1
    for index, argname in enumerate(funcspec.args):
        if index >= len(args): break
        result[argname] = args[index]
        pass
    index += 1
    varargs = args[index:]
    
    # bind kwargs
    keywords = {}
    for key, value in kwargs.items():
        if key in result: return None # dup names
        if key in funcspec.args:
            result[key] = value
            pass
        else:
            keywords[key] = value
            pass
        pass
    
    # bind defaults
    rdefaults = (funcspec.defaults or tuple())[::-1]
    rargnames = funcspec.args[::-1]
    for i in range(len(rdefaults)):
        argname = rargnames[i]
        if argname not in result: result[argname] = rdefaults[i]
        pass
    
    # check bound all args
    for argname in funcspec.args:
        if argname not in result: return None # lack
        pass
    
    if funcspec.varargs:
        result[funcspec.varargs] = varargs
        pass
    else:
        if varargs: return None
        pass
    
    if funcspec.keywords:
        result[funcspec.keywords] = keywords
        pass
    else:
        if keywords: return None
        pass
    
    return result
