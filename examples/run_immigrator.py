"""
An example call script that performs a single static VASP calculation.

Performs a self consistent electron convergence run using the standard silicon structure.
"""
# pylint: disable=too-many-arguments
from aiida.orm import Code
from aiida.plugins import CalculationFactory
from aiida.engine import submit
from aiida import load_profile

from aiida_vasp.utils.fixtures.testdata import data_path
load_profile()


def main(code_string, resources, folder):
    """Main method to setup the calculation."""

    # Set code from string
    code = Code.get_from_string(code_string)

    # Set up the process and inputs for the immigration.
    process, inputs = CalculationFactory('vasp.vasp').immigrant(code, folder, potential_family='pbe', resources=resources)
    submit(process, **inputs)


if __name__ == '__main__':
    # Code_string is chosen among the list given by 'verdi code list'
    CODE_STRING = 'vasp5@localhost'

    # Resources
    RESOURCES = {'num_machines': 1, 'num_mpiprocs_per_machine': 1}

    # Folder where the previous VASP calculation is placed
    FOLDER = data_path('basic_relax')

    main(CODE_STRING, RESOURCES, FOLDER)
