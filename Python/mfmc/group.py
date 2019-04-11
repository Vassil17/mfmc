from collections.abc import MutableMapping

from .exceptions import RequiredDatafieldError, OptionalDatafieldError


class Group(MutableMapping):
    _MANDATORY_DATASETS = []
    _MANDATORY_ATTRS = []
    _OPTIONAL_DATASETS = []
    _OPTIONAL_ATTRS = []

    def __init__(self):
        self._group = NotImplemented
        self._number = NotImplemented
        self._name = NotImplemented

    def __getitem__(self, key):
        key = key.upper()

        try:
            if key in self._MANDATORY_DATASETS + self._OPTIONAL_DATASETS:
                return self._decode_data(self._group[key])
            elif key in self._MANDATORY_ATTRS + self._OPTIONAL_ATTRS:
                return self._decode_data(self._group.attrs[key])
            else:
                raise KeyError(f"Unknown datafield name: {key}")
        except KeyError:
            if key in self._MANDATORY_DATASETS + self._MANDATORY_ATTRS:
                raise RequiredDatafieldError(key)
            elif key in self._OPTIONAL_DATASETS + self._OPTIONAL_ATTRS:
                raise OptionalDatafieldError(key)

    def __setitem__(self, key, value):
        raise NotImplementedError("Writing data is not supported yet")

    def __delitem__(self, key):
        raise NotImplementedError("Deleting data is not supported yet")

    def __len__(self):
        return len(self.keys())

    def __iter__(self):
        return iter(self.keys())

    @classmethod
    def is_mandatory(cls, datafield):
        item = datafield.upper()
        return item in cls._MANDATORY_DATASETS + cls._MANDATORY_ATTRS

    @classmethod
    def is_optional(cls, datafield):
        item = datafield.upper()
        return item in cls._OPTIONAL_DATASETS + cls._OPTIONAL_ATTRS

    @staticmethod
    def _decode_data(data):
        if isinstance(data, bytes):
            return data.decode('ascii')
        else:
            return data

    @property
    def user_attributes(self):
        ret = {}
        for k, v in self._group.attrs.items():
            if k not in self._MANDATORY_ATTRS + self._OPTIONAL_ATTRS:
                ret[k] = self._decode_data(v)
        return ret

    @property
    def user_datasets(self):
        ret = {}
        for k, v in self._group.items():
            if k not in self._MANDATORY_DATASETS + self._OPTIONAL_DATASETS:
                ret[k] = self._decode_data(v)
        return ret

    @property
    def number(self):
        return self._num

    @property
    def name(self):
        return self._name
