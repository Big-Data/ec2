#coding=utf-8

import time, sys, os
import types

def isfunction(object):
    """Return true if the object is a user-defined function.

    Function objects provide these attributes:
        __doc__         documentation string
        __name__        name with which this function was defined
        func_code       code object containing compiled function bytecode
        func_defaults   tuple of any default values for arguments
        func_doc        (same as __doc__)
        func_globals    global namespace in which this function was defined
        func_name       (same as __name__)"""
    return isinstance(object, types.FunctionType)

def isclass(object):
    """Return true if the object is a class.

    Class objects provide these attributes:
        __doc__         documentation string
        __module__      name of module in which this class was defined"""
    return isinstance(object, types.ClassType) or hasattr(object, '__bases__')


def my_import(name):
    """Helper function for walking import calls when searching for classes by
    string names.
    """
    mod = __import__(name, {}, {}, ['']) 
    #components = name.split('.')
    #for comp in components[1:]:
    #    mod = getattr(mod, comp)
    return mod

def safe_str_to_class(s):
    """Helper function to map string class names to module classes."""
    lst = s.split(".")
    klass = lst[-1]
    mod_list = lst[:-1]
    module = ".".join(mod_list)
    mod = my_import(module)
    if hasattr(mod, klass):
        return getattr(mod, klass)
    else:
        raise ImportError('')


def load_module(name, reload=False,auto_reload=False):
    if reload and sys.modules.has_key(name):
        del sys.modules[name]

    mod = sys.modules.get(name, None)
    if auto_reload and mod and hasattr(mod, 'loadtime'):
        ftime = os.path.getmtime(mod.__file__.replace('.pyc','.py'))
        if mod.loadtime<ftime:
            del sys.modules[name]
            mod = None
    
    if not mod:
        try:
            mod = __import__(name, {}, {}, ['']) 
        except ImportError:
            return            
    
    if mod and not hasattr(mod, 'loadtime'): 
        ftime = os.path.getmtime(mod.__file__.replace('.pyc','.py'))
        mod.loadtime = ftime
    return mod

def str_to_class(s, reload=False, auto_reload=False):
    """Alternate helper function to map string class names to module classes."""
    lst = s.split(".")
    klass = lst[-1]
    module = ".".join(lst[:-1])
    if not module: return

    mod = load_module(module, reload, auto_reload)
    if mod and hasattr(mod, klass):
        return getattr(mod, klass)


def walk_modules(path, load=False):
    """Loads a module and all its submodules from a the given module path and
    returns them. If *any* module throws an exception while importing, that
    exception is thrown back.

    For example: walk_modules('scrapy.utils')
    """

    mods = []
    mod = __import__(path, {}, {}, [''])
    mods.append(mod)
    if hasattr(mod, '__path__'):
        for _, subpath, ispkg in iter_modules(mod.__path__):
            fullpath = path + '.' + subpath
            if ispkg:
                mods += walk_modules(fullpath)
            else:
                submod = __import__(fullpath, {}, {}, [''])
                mods.append(submod)
    return mods


if __name__=='__main__':
    pass

