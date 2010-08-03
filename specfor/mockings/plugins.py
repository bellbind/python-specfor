import inspect

class Restriction(object):
    name = "nop"
    def __repr__(self):
        return "[]"
    def precalled(self, responsibilities, *args, **kwargs):
        """called before method calling
        """
        return True
    def postcalled(self, responsibilities, returns, *args, **kwargs):
        """called after method calling
        """
        return True
    def completed(self, responsibilities):
        """called when mock completed check
        raise AssertError if restriction does not completed
        """
        return
    pass

plugins = []

def register(key, restrection_factory):
    plugins.append((key, restrection_factory))
    pass

def to_restrictions(responsibility, kwargs):
    restrictions = []
    for key, restrection_factory in plugins:
        if key in kwargs:
            rest = restrection_factory(responsibility, kwargs[key])
            restrictions.append(rest)
            pass
        pass
    return restrictions
