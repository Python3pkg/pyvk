# -*- coding: utf-8 -*-
"""
    pyvk.exceptions
    ~~~~~~~~~~~~~~~

    Implements custom exceptions.

    :copyright: (c) 2013-2016, Max Kuznetsov
    :license: MIT, see LICENSE for more details.
"""





class PyVKError(Exception):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__,
                               ', '.join(map(repr, self.args)),
                               ', '.join("%s=%s" % (k, repr(v)) for k,v in list(self.kwargs.items())))

    __str__ = __repr__

    def __getattr__(self, name):
        return self.kwargs[name]

    __getitem__ = __getattr__


class AuthError(PyVKError):
    pass


class InvalidToken(PyVKError):
    pass


class ReqError(PyVKError):
    pass


class APIError(PyVKError):
    pass
