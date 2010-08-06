"""compatibilities for old python
"""

def arg_parser(argname, **kwargs):
    try:
        # for python2.7
        import argparse
        return ParserArgParse(argname, **kwargs)
    except:
        return ParserOptParse(argname, **kwargs)
    pass

class ParserOptParse(object):
    def __init__(self, argname, **kwargs):
        import optparse
        usage = "%prog [options] [" + argname + " [" + argname + "...]]"
        kwargs["usage"] = usage
        self.parser = optparse.OptionParser(**kwargs)
        pass
    def add(self, *args, **kwargs):
        self.parser.add_option(*args, **kwargs)
        pass
    def parse(self, *args):
        return self.parser.parse_args(*args)
    pass

class ParserArgParse(object):
    def __init__(self, argname, **kwargs):
        self.argname = argname
        import argparse
        version = None
        if "version" in kwargs:
            version = kwargs["version"]
            del kwargs["version"]
            pass
        self.parser = argparse.ArgumentParser(**kwargs)
        if version: 
            self.parser.add_argument(
                '--version', action='version', version=version)
            pass
        self.parser.add_argument(argname, nargs="*")
        pass
    def add(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)
        pass
    def parse(self, *args):
        opts = self.parser.parse_args(*args)
        args = getattr(opts, self.argname)
        return opts, args
    pass
