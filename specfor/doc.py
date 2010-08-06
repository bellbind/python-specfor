from __future__ import with_statement
import os

def main():
    from specfor import version 
    from specfor.compat import arg_parser
    from specfor.docs import simple
    from specfor.docs import plugins
    
    parser = arg_parser(
        "module.name",
        description="Generate documents from specfor spec defined modules.",
        version=version)
    parser.add(
        "-n", "--name", dest="name", default="simple",
        help="document generator name (default: simple)")
    parser.add(
        "-x", "--ext", dest="ext", default="md",
        help="generated file ext (default: md)")
    opts, modnames = parser.parse()
    
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
