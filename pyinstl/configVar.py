#!/usr/local/bin/python3

from __future__ import print_function

"""
    Copyright (c) 2012, Shai Shasag
    All rights reserved.
    Licensed under BSD 3 clause license, see LICENSE file for details.
"""

import os
import sys


class ConfigVar(object):
    """ Keep a single, named, config variable and it's values.
        Also info about where it came from (file, line).
        value may have $() style references to other variables.
        Values are always a list - even a single value is a list of size 1
        Emulates list container
    """
    __slots__ = ("_name", "_description", "_values", "__resolving_in_progress")
    def __init__(self, name, description="", *values):
        self._name = name
        self._description = description
        self._values = list(values)
        self.__resolving_in_progress = False # prevent circular resolves

    def name(self):
        """ return the name of this variable """
        return self._name

    def description(self):
        """ return the description of this variable """
        return self._description

    def set_description(self, description):
        """ Assign new description """
        self._description = description

    def __str__(self):
        ln = os.linesep
        indent = "    "
        retVal = "{self._name}:{ln}{indent}description:{self._description}{ln}{indent}values:{self._values})".format(**vars())
        return retVal

    def __repr__(self):
        retVal = "{self.__class__.__name__}('{self._name}', '{self._description}',*{self._values})".format(**vars())
        return retVal

    def __len__(self):
        return len(self._values)

    def __getitem__(self, key):
        # if key is of invalid type or value, the list values will raise the error
        return self._values[key]

    def __setitem__(self, key, value):
        self._values[key] = value

    def __delitem__(self, key):
        del self._values[key]

    def __iter__(self):
        return iter(self._values)

    def __reversed__(self):
        return reversed(self._values)

    def append(self, value):
        self._values.append(value)

    def extend(self, value):
        self._values.extend(value)

class ConstConfigVar(ConfigVar):
    """ ConfigVar override where values cannot be changed after construction """
    __slots__ = ()
    def __init__(self, name, description="", *values):
        if sys.version_info < (3, 0):
            super(ConstConfigVar, self).__init__(name, description, *values)
        else:
            super().__init__(name, description, *values)

    def set_description(self, description):
        raise Exception("Cannot change a const value", self._name)

    def __setitem__(self, key, value):
        raise Exception("Cannot change a const value", self._name)

    def __delitem__(self, key):
        raise Exception("Cannot change a const value", self._name)

    def append(self, value):
        raise Exception("Cannot change a const value", self._name)

    def extend(self, value):
        raise Exception("Cannot change a const value", self._name)

if __name__ == "__main__":
    pass
