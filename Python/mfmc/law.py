from .group import Group


class Law(Group):
    _MANDATORY_DATASETS = ['PROBE', 'ELEMENT']
    _MANDATORY_ATTRS = ['TYPE']
    _OPTIONAL_DATASETS = ['DELAY', 'WEIGHTING']
    _OPTIONAL_ATTRS = []

    def __init__(self, group):
        self._group = group
