"""
Parameter related utils

-----------------------
Contains utils and definitions that are used together with the parameters.
"""
import enum

from aiida.common.extendeddicts import AttributeDict


def find_key_in_dicts(dictionary, key):
    """Find a key in a nested dictionary."""
    for k, v in dictionary.items():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find_key_in_dicts(v, key):
                yield result


class RelaxAlgoEnum(enum.IntEnum):
    """Encode values for algorithm descriptively in enum."""
    NO_UPDATE = -1
    IONIC_RELAXATION_RMM_DIIS = 1
    IONIC_RELAXATION_CG = 2


class RelaxModeEnum(enum.IntEnum):
    """
    Encode values for mode of relaxation descriptively in enum.

    Values can be found here: https://cms.mpi.univie.ac.at/wiki/index.php/ISIF
    """

    POS_ONLY = 2
    POS_SHAPE_VOL = 3
    POS_SHAPE = 4
    SHAPE_ONLY = 5
    SHAPE_VOL = 6
    VOL_ONLY = 7

    @classmethod
    def get_from_dof(cls, **kwargs):
        """Get the correct mode of relaxation for the given degrees of freedom."""
        RELAX_POSSIBILITIES = ('positions', 'shape', 'volume')  # pylint: disable=invalid-name
        dof = tuple(kwargs[i] for i in RELAX_POSSIBILITIES)
        value_from_dof = {
            (True, False, False): cls.POS_ONLY,
            (True, True, True): cls.POS_SHAPE_VOL,
            (True, True, False): cls.POS_SHAPE,
            (False, True, False): cls.SHAPE_ONLY,
            (False, True, True): cls.SHAPE_VOL,
            (False, False, True): cls.VOL_ONLY
        }
        try:
            return value_from_dof[dof]
        except KeyError:
            raise ValueError('Invalid combination for degrees of freedom: {}'.format(dict(zip(RELAX_POSSIBILITIES, dof))))


class ParametersMassage():

    def __init__(self, calc, parameters):
        self._calc = calc
        self._massage = AttributeDict()
        self._parameters = parameters
        self._load_valid_params()
        self._functions = ParameterSetFunctions(self._calc, self._parameters, self._massage)
        self._prepare_parameters()
        self._check_parameters()

    def _load_valid_params(self):
        from os import path
        from yaml import safe_load
        params = None
        with open(path.join(path.dirname(path.realpath(__file__)), 'tags.yml'), 'r') as file_handler:
            tags_data = safe_load(file_handler)
        self._valid_parameters = list(tags_data.keys())

    def _build_function_loader(self):
        function_loader = {}
        for key in self._valid_parameters:
            function_loader[key] = 'set_' + key
        self._function_loader = function_loader

    def _prepare_parameters(self):
        for key in self._valid_parameters:
            self._set(key)

    def _check_parameters(self):
        """Make sure all the massaged values are to VASP spec."""
        if list(self._massage.keys()).sort() != self._valid_parameters.sort():
            self._calc.exit_codes.ERROR_INVALID_PARAMETER_DETECTED

    def _set(self, key):
        """Call the necessary function to set each parameter."""
        try:
            getattr(self._functions, 'set_' + key)()
        except AttributeError:
            pass
        # If we find any raw code input key directly on parameter root, override whatever we have set until now
        # Also, make sure it is lowercase
        if self._parameters.get(key) or self._parameters.get(key.upper()):
            self._massage[key] = self._parameters[key]

    @property
    def parameters(self):
        """Return the massaged parameter set ready to go in VASP format."""
        return self._massage


class ParameterSetFunctions():

    def __init__(self, calc, parameters, massage):
        self._parameters = parameters
        self._calc = calc
        self._massage = massage

    def set_ibrion(self):
        """Set which algorithm to use for ionic movements."""
        if self._relax():
            try:
                if self._parameters.relax.algo == 'cg':
                    self._massage.ibrion = RelaxAlgoEnum.IONIC_RELAXATION_CG.value
                elif self._parameters.relax.algo == 'rd':
                    self._massage.ibrion = RelaxAlgoEnum.IONIC_RELAXATION_RMM_DIIS.value
            except AttributeError:
                self._massage.ibrion = RelaxAlgoEnum.NO_UPDATE.value

    def set_ediffg(self):
        """Set the cutoff to use for relaxation."""
        if not self._relax():
            return
        energy_cutoff = False
        try:
            self._massage.ediffg = self._parameters.relax.energy_cutoff
            energy_cutoff = True
        except AttributeError:
            pass
        try:
            self._massage.ediffg = -abs(self._parameters.relax.force_cutoff)
            if energy_cutoff:
                self._calc.report('User supplied both a force and an energy cutoff for the relaxation. Utilizing the force cutoff.')
        except AttributeError:
            pass

    def set_nsw(self):
        """Set the number of ionic steps to perform."""
        if self._relax():
            self._set_simple('nsw', self._parameters.relax.steps)

    def set_isif(self):
        """Set relaxation mode according to the chosen degrees of freedom."""
        positions = self._parameters.get('relax', {}).get('positions', False)
        shape = self._parameters.get('relax', {}).get('shape', False)
        volume = self._parameters.get('relax', {}).get('volume', False)
        if positions or shape or volume:
            self._massage.isif = RelaxModeEnum.get_from_dof(positions=positions, shape=shape, volume=volume).value

    def _relax(self):
        """Check if we have enabled relaxation."""
        return self._parameters.get('relax', {}).get('positions') or \
            self._parameters.get('relax', {}).get('shape') or \
            self._parameters.get('relax', {}).get('volume')

    def _set_simple(self, target, value):
        """Set basic parameter."""
        try:
            self._massage[target] = value
        except AttributeError:
            pass
