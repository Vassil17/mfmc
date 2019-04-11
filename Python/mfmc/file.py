from os.path import isfile
import re
from typing import List

import h5py

from .group import Group
from .probe import Probe
from .sequence import Sequence


class File(Group):
    _PROBE_RE = re.compile(r'PROBE<\d+>')
    _SEQUENCE_RE = re.compile(r'SEQUENCE<\d+>')
    _MFMC_TYPE = b'MFMC'
    _MFMC_VERSION = b'2.0.0'
    _MANDATORY_ATTRS = ['TYPE', 'VERSION']

    def __init__(self, filename: str) -> None:
        """A wrapper around an MFMC file.

        This enumerates the probes and sequences which are contained in the file.
        A file will be created if the filename is not found.

        Parameters
        ----------
        filename
            The filename of the HDF5.
        """
        self._file = h5py.File(filename)
        self._group = self._file

        if isfile(filename):
            # If file exists, check required datafields
            try:
                if (self._file.attrs['TYPE'] != File._MFMC_TYPE):
                    raise ValueError("File does not contain MFMC data")
                if (self._file.attrs['VERSION'] != File._MFMC_VERSION):
                    raise ValueError("Unsupported version")
            except KeyError:
                raise ValueError("File does not contain MFMC data")

            self._probes = [Probe(v) for k, v in self._file.items()
                if File._PROBE_RE.match(k)]
            self._sequences = [Sequence(v) for k, v in self._file.items()
                if File._SEQUENCE_RE.match(k)]
        else:
            self._file.attrs['TYPE'] = File._MFMC_TYPE
            self._file.attrs['VERSION'] = File._MFMC_VERSION

    def close(self) -> None:
        """Closes a MFMC file."""
        self._file.close()

    @property
    def probes(self) -> List[Probe]:
        """A list of the probes defined in the file."""
        return self._probes

    @property
    def sequences(self) -> List[Probe]:
        """A list of the sequences defined in the file."""
        return self._sequences
