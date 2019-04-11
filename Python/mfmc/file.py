from os.path import isfile
import re

import h5py

from .probe import Probe
from .sequence import Sequence


class File:
    _PROBE_RE = re.compile(r'PROBE<\d+>')
    _SEQUENCE_RE = re.compile(r'SEQUENCE<\d+>')
    _MFMC_TYPE = b'MFMC'
    _MFMC_VERSION = b'2.0.0'

    def __init__(self, filename):
        self._file = h5py.File(filename)

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

    def close(self):
        self._file.close()

    @property
    def version(self):
        version = self._file.attrs['VERSION']
        return version.decode('ascii')

    @property
    def probes(self):
        return self._probes

    @property
    def sequences(self):
        return self._sequences
