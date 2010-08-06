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
        "-d", "--dest", dest="dest", default=".",
        help="directory for generated docs (default: )")
    parser.add(
        "-n", "--name", dest="name", default="simple",
        help="document generator name (default: simple)")
    parser.add(
        "-x", "--ext", dest="ext", default="md",
        help="generated file ext (default: md)")
    opts, modnames = parser.parse()
    
    if not os.path.isdir(opts.dest): os.makedirs(opts.dest)
    for modname in modnames:
        if os.path.isfile(modname):
            modname = f2m(modname)
            if not modname: continue
            pass
        module = __import__(modname, fromlist=["*"])
        outname = os.path.join(
            opts.dest, "%s%s%s" % (modname, os.path.extsep, opts.ext))
        
        print("write: %s" % outname)
        with open(outname, "w") as f:
            for line in plugins.convert(opts.name, opts, module):
                f.write(line)
                pass
            f.flush()
            pass
        pass
    pass

def f2m(filename):
    names = os.path.normpath(filename).split(os.path.sep)
    name, ext = os.path.splitext(names[-1])
    if ext != ".py": return None
    if name == "__init__": return ".".join(names[:-1])
    return ".".join(names[:-1] + [name])

if __name__ == "__main__": main()
