try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


try:
    from struct import Struct as Packer
except ImportError:
    from struct import pack, unpack, calcsize
    class Packer(object):
        __slots__ = ["format", "size"]
        def __init__(self, format):
            self.format = format
            self.size = calcsize(format)
        def pack(self, *args):
            return pack(self.format, *args)
        def unpack(self, data):
            return unpack(self.format, data)

import reconstruct

def subs(c):
    if hasattr(c, 'subcons'):
        return c.subcons
    else:
        return []

def container_diff(first_c, second_c, construct, path=None):
    first_keys = set(first_c.__dict__.keys())
    second_keys = set(second_c.__dict__.keys())
    first_no_second = first_keys - second_keys
    second_no_first = second_keys - first_keys
    both = first_keys & second_keys
    if not path:
        path = [construct.name]
    def get_path(k):
        return '.'.join(path+[k])
    for c in subs(construct):
        k = c.name
        if k in first_no_second:
            print '%s not in second' % get_path(k)
        if k in second_no_first:
            print '%s not in first' % get_path(k)
        if k in both:
            first = getattr(first_c, k)
            second = getattr(second_c, k)
            if isinstance(first, reconstruct.Container):
                container_diff(first, second, c, path+[k])
            elif first != second:
                print '%s mismatched between' % get_path(k)
                print '   first', first
                print '   second', second
            else:
                print '%s the same' % get_path(k)


