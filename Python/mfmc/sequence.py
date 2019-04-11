import re

from .group import Group
from .law import Law


class Sequence(Group):
    _MANDATORY_DATASETS = [
        'MFMC_DATA',
        'PROBE_PLACEMENT_INDEX',
        'PROBE_POSITION',
        'PROBE_X_DIRECTION',
        'PROBE_Y_DIRECTION',
        'TRANSMIT_LAW',
        'RECEIVE_LAW',
        'PROBE_LIST'
    ]
    _MANDATORY_ATTRS = [
        'TYPE',
        'TIME_STEP',
        'START_TIME',
        'SPECIMEN_VELOCITY'
    ]
    _OPTIONAL_DATASETS = ['MFMC_DATA_IM', 'DAC_CURVE']
    _OPTIONAL_ATTRS = [
        'WEDGE_VELOCITY',
        'TAG',
        'RECEIVER_AMPLIFIER_GAIN',
        'FILTER_TYPE',
        'FILTER_PARAMETERS',
        'FILTER_DESCRIPTION',
        'OPERATOR',
        'DATE_AND_TIME'
    ]
    _SEQUENCE_RE = re.compile(r'\/SEQUENCE<(\d+)>')
    _LAW_RE = re.compile(r'LAW<\d+>')

    def __init__(self, group):
        self._name = group.name
        self._group = group
        self._num = self._SEQUENCE_RE.match(group.name).group(1)

        self._laws = [Law(v) for k, v in self._group.items()
           if self._LAW_RE.match(k)]

    @property
    def laws(self):
        return self._laws
