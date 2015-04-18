
class SchemaError(BaseException):
    pass

class Validator(object):
    def __init__(self, default=None, help=''):
        self._default = default
        self.help = help
        self.name = 'unnamed'

    def default(self):
        if self._default is None:
            raise SchemaError('no value was provided for item {}, but this item does not have a default.'.format(self.name))
        return self._default

class Schema(Validator):
    def validate(self, d):
        '''takes a dictionary and returns the validated dictionary, filling in defaults'''
        retval = {}
        for k, v in self.items():
            if k in d:
                retval[k] = v.validate(d[k])
            else:
                retval[k] = v.validate(v.default())
        return retval

    def __getitem__(self, name):
        return getattr(self, name).to_python()

    def items(self):
        objs = [(obj, getattr(self, obj)) for obj in dir(self)]
        valid_objs = filter(lambda obj: isinstance(obj[1], Validator), objs)
        for name, obj in valid_objs:
            obj.name = name
        return valid_objs

    def default(self):
        return {k: v.default() for k, v in self.items()}

class Int(Validator):
    def validate(self, v):
        return int(v)

class Float(Validator):
    def validate(self, v):
        return float(v)

class String(Validator):
    def validate(self, v):
        return str(v)

class WorkingDir(Validator):
    def validate(self, v):
        return v

    def default(self):
        import os
        return os.getcwd()

class List(Validator):
    def __init__(self, validator, default=None):
        super(List, self).__init__(default=default)
        self._validator = validator

    def validate(self, vlist):
        return [self._validator.validate(v) for v in vlist]
