# -*- coding: utf-8 -*-
"""
    pyvk.utils
    ~~~~~~~~~~

    Implements various utility classes and functions.

    :copyright: (c) 2013-2016 by Max Kuznetsov.
    :license: MIT, see LICENSE for more details.
"""

from collections import Mapping
import getpass
import sys


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


if PY2:  # pragma: no cover
    from itertools import izip
    input = raw_input
    zip = izip
else:  # pragma: no cover
    zip = zip


def accumulate(iterable):
    it = iter(iterable)

    try:
        total = next(it)
        yield total
    except StopIteration:
        return

    for element in it:
        total += element
        yield total


def filter_dict(d):
    # Remove None values
    return dict(filter(lambda x: x[1] is not None,
                       d.items()))


def process_args(args):

    def convert(item):
        if type(item) is list:
            # Transform lists into comma-separated strings
            return ','.join(str(x) for x in item)
        elif type(item) is bool:
            # Transform Booleans into 0 and 1
            return int(item)
        else:
            return item

    return filter_dict(dict((k, convert(v)) for k, v in args.items()))


def setup_logger(config):
    import logging
    log_file = {'filename': config.log_file} \
        if config.log_file else {}
    logging.basicConfig(format=config.log_format,
                        level=config.log_level, **log_file)


class Config(Mapping):
    _lock = False
    _len = None

    def __init__(self, **params):
        for attr, value in params.items():
            setattr(self, attr, value)
        self._len = len(list(self.__iter__()))

        # Make attributes read-only
        self._lock = True

    def __getitem__(self, item):
        return getattr(self, item)

    def __len__(self):
        return self._len

    def __iter__(self):
        def is_param(attr):
            return not (attr.startswith('_') or callable(getattr(self, attr)))
        return (attr for attr in dir(self) if is_param(attr))

    def __repr__(self):
        params = ', '.join('%s=%s' % (k, repr(v)) for k, v in self.items())
        return '{name}({params})'.format(name=self.__class__.__name__,
                                         params=params)

    def __setattr__(self, attr, value):
        if self._lock:
            raise AttributeError('Cannot assign attributes to this class')

        if attr in dir(self):
            self.__dict__[attr] = value

        # Ignore undefined parameters
        else:
            pass


class Input(object):

    @staticmethod
    def prompt(prompt):
        return input(prompt).strip()

    @staticmethod
    def ask(field, **kwargs):

        if field == 'username':
            return Input.prompt('Username (email of mobile number): ')

        elif field == 'app_id':
            return Input.prompt('API ID: ')

        elif field == 'password':
            return getpass.getpass('Password: ')

        elif field == 'secret_code':
            return Input.prompt('Secret code: ')

        elif field == 'phone':
            try:
                return Input.prompt('%s: ' % kwargs['msg'])
            except KeyError:
                raise ValueError('Message is not provided')

        elif field == 'captcha':
            try:
                text = "%s\nEnter text from the picture above: " % kwargs['img']
                return Input.prompt(text)
            except KeyError:
                raise ValueError('Image URL is not provided')

        else:
            raise ValueError('Unknown field')
