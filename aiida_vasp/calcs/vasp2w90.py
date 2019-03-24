# pylint: disable=abstract-method
# explanation: pylint wrongly complains about (aiida) Node not implementing query
"""VASP2Wannier90 - Calculation"""
from aiida.plugins import DataFactory
from aiida.orm import List

from aiida_wannier90.io import write_win
from aiida_vasp.calcs.base import Input
from aiida_vasp.calcs.vasp import VaspCalculation


class Vasp2w90Calculation(VaspCalculation):
    """General purpose Calculation for using vasp with the vasp2wannier90 interface."""

    _default_parser = 'vasp.vasp2w90'
    _DEFAULT_PARAMETERS = {'lwannier90': True}

    @classmethod
    def define(cls, spec):
        super(Vasp2w90Calculation, cls).define(spec)
        spec.input('wannier_parameters', valid_type=get_data_class('parameter'), help='Input parameters for the Wannier90 interface.')
        spec.input(
            'wannier_projections',
            valid_type=(get_data_class('orbital'), List),
            help='Projections to be defined in the Wannier90 input file.')

    def write_win(self, dst):
        """Write Wannier90 input file"""
        write_win(
            filename=dst, parameters=self.inputs.get('wannier_parameters', {}), projections=self.inputs.get('wannier_projections', None))

    @staticmethod
    def new_wannier_parameters(**kwargs):
        return DataFactory('parameter')(**kwargs)

    def write_additional(self, tempfolder):
        super(Vasp2w90Calculation, self).write_additional(tempfolder)
        win = tempfolder.get_abs_path('wannier90.win')
        self.write_win(win)
