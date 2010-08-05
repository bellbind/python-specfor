import optparse
import os
from .docs import simple
from .docs import plugins


def main():
    parser = optparse.OptionParser(
        usage="\n".join(
            ["%prog [opts] module.name ...",
             "",
             "Generate documents from specfor spec defined modules."]))
    parser.add_option(
        "-n", "--name", dest="name", default="simple",
        help="document generator name (default: %default)")
    parser.add_option(
        "-x", "--ext", dest="ext", default="md",
        help="generated file ext (default: %default)")
    opts, modnames = parser.parse_args()
    
    for modname in modnames:
        module = __import__(modname, fromlist=["*"])
        with open("%s%s%s" % (modname, os.path.extsep, opts.ext), "w") as f:
            for line in plugins.convert(opts.name, opts, module):
                f.write(line)
                pass
            f.flush()
            pass
        pass
    pass

if __name__ == "__main__": main()
