import re

from .group import Group


class Probe(Group):
    _MANDATORY_DATASETS = [
        'ELEMENT_POSITION',
        'ELEMENT_MINOR',
        'ELEMENT_MAJOR',
        'ELEMENT_SHAPE'
    ]
    _MANDATORY_ATTRS = ['TYPE', 'CENTRE_FREQUENCY']
    _OPTIONAL_DATASETS = [
        'ELEMENT_RADIUS_OF_CURVATURE',
        'ELEMENT_AXIS_OF_CURVATURE',
        'DEAD_ELEMENT'
    ]
    _OPTIONAL_ATTRS = [
        'WEDGE_SURFACE_POINT',
        'WEDGE_SURFACE_NORMAL',
        'BANDWIDTH',
        'PROBE_MANUFACTURER',
        'PROBE_SERIAL_NUMBER',
        'PROBE_TAG',
        'WEDGE_MANUFACTURER',
        'WEDGE_SERIAL_NUMBER',
        'WEDGE_TAG'
    ]
    _PROBE_RE = re.compile(r'\/PROBE<(\d+)>')

    def __init__(self, group):
        """Representation of a probe from a MFMC file.

        Parameters
        ----------
        group : h5py.Group
            The h5py group for the probe.
        """
        self._name = group.name
        self._group = group
        self._num = self._PROBE_RE.match(group.name).group(1)
