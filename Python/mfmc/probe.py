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

    @staticmethod
    def _set_datafield(group, name, datafields, attr=False):
        try:
            data = datafields[name.lower()]
            if isinstance(data, str):
                data = data.encode('ascii')
        except KeyError:
            return
        else:
            if attr:
                group.attrs[name] = datafields[name.lower()]
            else:
                group[name] = datafields[name.lower()]

    @staticmethod
    def create_probe(file, num: int, datafields: Dict[str, Any]) -> Probe:
        # First, check mandatory ones are there
        missing = [e for e in self._MANDATORY_ATTRS + self._MANDATORY_DATASETS
                   if e not in datafields.keys()]
        if missing:
            raise ValueError(f"Required datafields not set: {missing}")
            return None

        name = f'PROBE<{num}>'
        group = file.create_group(name)

        for a in self._MANDATORY_ATTRS + self._OPTIONAL_ATTRS:
            self._set_datafield(group, a, datafields, True)
        for d in self._MANDATORY_DATASETS + self._OPTIONAL_DATASETS:
            self._set_datafield(group, d, datafields)
