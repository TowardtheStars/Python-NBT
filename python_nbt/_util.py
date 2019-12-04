

class RestrictedDict(dict):

    def __init__(self, value_validator=None, key_validator=None, iterable=None):
        super().__init__()
        if not value_validator:
            self._validate_value = lambda value: True
        else:
            if not callable(value_validator):
                raise "value_validator should be callable or None"
            self._validate_value = value_validator
        if not key_validator:
            self._validate_key = lambda key: True
        else:
            if not callable(key_validator):
                raise "key_validator should be callable or None"
            self._validate_key = key_validator
        if iterable:
            self.update(iterable)

    
    def __setitem__(self, key, value):
        if not self._validate_key(key):
            raise "Invalid key type, need %s but get %s" % ((t.__name__ for t in self._key_types), type(key))
        if not self._validate_value(value):
            raise "Invalid value type, need %s but get %s" % ((t.__name__ for t in self._types), type(value))
        return super().__setitem__(key, value)

    def can_merge(self, _dict):
        return isinstance(_dict, dict) and all([self._validate_key(k) and self._validate_value(v) for k, v in _dict])

    def trim(self, _dict):
        """
        trim dictionary to fit a form like self
        """
        return { k : v for k, v in _dict if self._validate_key(k) and self._validate_value(v) }

    def update(self, d, trim=False):
        if trim:
            d = self.trim(d)
        if not self.can_merge(d):
            raise "Cannot update dict because there are invalid keys or values in %s" % str(d)
        return super().update(d)


class TypeRestrictedDict(RestrictedDict):

    def __init__(self, value_types=None, key_types=None, iterable=None):
        """
        @var: acceptable_types: Types that can be a value of this dict
        @var: key_types: Types that can be a key of this dict
        """
        self._types = (tuple(value_types) if not isinstance(value_types, type) else (value_types, )) if value_types else None
        self._key_types = (tuple(key_types) if not isinstance(key_types, type) else (key_types, )) if key_types else None
        super(TypeRestrictedDict, self).__init__(
            key_validator=lambda key: isinstance(key, self._key_types) if self._key_types else True,
            value_validator=lambda value: isinstance(value, self._types) if self._types else True
        )

    @property
    def types(self):
        return self._types

    @property
    def key_types(self):
        return self._key_types


class RestrictedList(list):
    
    def __init__(self, validator=None, iterable=None, trim=True):
        if validator:
            self._validate = validator
        elif callable(validator):
            self._validate = lambda value : True
        else:
            raise TypeError("Validator must be callable!")
        if iterable:
            self.extend(iterable, trim=trim)
    
    def append(self, obj):
        if not self._validate(obj):
            raise "Value %s can not put in this RestrictList" % str(obj)
        return super().append(obj)

    def insert(self, index, obj):
        if not self._validate(obj):
            raise "Value %s can not put in this RestrictList" % str(obj)
        return super().insert(index, obj)

    def extend(self, iterable, trim=False):
        if not trim:
            cond = map(self._validate, iterable)
            if not all(cond):
                raise "Contains value that cannot be put into this RestricList"
        else:
            iterable = [o for o in iterable if self._validate(o)]
        return super().extend(iterable)


class TypeRestrictedList(RestrictedList):

    def __init__(self, types=None):
        self._types = (tuple(types) if not isinstance(types, type) else (types, )) if types else None
        super().__init__(validator=lambda value: isinstance(value, self._types) if self._types else True)
        
    @property
    def types(self):
        return self._types


        