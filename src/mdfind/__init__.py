__all__ = ['mdfind', 'count', 'name', 'query']


import runcmd
import values


def _args(query=None, name=None, onlyin=None):
    args = []
    if name:
        args += ["-name", name]
    for path in values.get(onlyin):
        args += ["-onlyin", path]
    if query:
        args += [query]
    return list(args)


def mdfind(args):
    """execute mdfind with arguments"""
    cmd = ["mdfind"] + list(args)
    return runcmd.run(cmd).exc().out


def count(query=None, name=None, onlyin=None):
    """return search results count"""
    args = ["-count"] + _args(query=query, name=name, onlyin=onlyin)
    return int(mdfind(args))


def name(name, onlyin=None):
    """`mdfind -name name` search by name"""
    args = _args(name=name, onlyin=onlyin)
    return mdfind(args).splitlines()


def query(query, onlyin=None):
    """search by Spotlight query"""
    args = _args(query=query, onlyin=onlyin)
    return mdfind(args).splitlines()
