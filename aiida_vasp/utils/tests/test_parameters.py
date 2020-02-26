"""Test aiida_parameters."""
# pylint: disable=unused-import,redefined-outer-name,unused-argument,unused-wildcard-import,wildcard-import,no-member

import pytest

from aiida.common.extendeddicts import AttributeDict

from aiida_vasp.utils.parameters import ParametersMassage


@pytest.fixture
def init_general_parameters():
    general_parameters = AttributeDict()
    general_parameters.relax = AttributeDict()
    general_parameters.relax.algo = 'cg'
    general_parameters.relax.energy_cutoff = 0.01
    general_parameters.relax.force_cutoff = 0.01
    general_parameters.relax.steps = 60
    general_parameters.relax.positions = True
    general_parameters.relax.shape = True
    general_parameters.relax.volume = True

    return general_parameters


def test_relax_parameters_all_set(init_general_parameters):
    massager = ParametersMassage(None, init_general_parameters)
    parameters = massager.parameters
    assert parameters.ediffg == -0.01
    assert parameters.ibrion == 2
    assert parameters.nsw == 60
    assert parameters.isif == 3


def test_relax_parameters_energy(init_general_parameters):
    del init_general_parameters.relax.force_cutoff
    massager = ParametersMassage(None, init_general_parameters)
    parameters = massager.parameters
    assert parameters.ediffg == 0.01


def test_relax_parameters_no_algo(init_general_parameters):
    del init_general_parameters.relax.algo
    massager = ParametersMassage(None, init_general_parameters)
    parameters = massager.parameters
    assert parameters.ibrion == -1


def test_relax_parameters_vol_shape(init_general_parameters):
    del init_general_parameters.relax.positions
    massager = ParametersMassage(None, init_general_parameters)
    parameters = massager.parameters
    assert parameters.isif == 6


def test_relax_parameters_pos_shape(init_general_parameters):
    del init_general_parameters.relax.volume
    massager = ParametersMassage(None, init_general_parameters)
    parameters = massager.parameters
    assert parameters.isif == 4


def test_relax_parameters_vol(init_general_parameters):
    del init_general_parameters.relax.positions
    del init_general_parameters.relax.shape
    massager = ParametersMassage(None, init_general_parameters)
    parameters = massager.parameters
    assert parameters.isif == 7


def test_relax_parameters_pos(init_general_parameters):
    del init_general_parameters.relax.volume
    del init_general_parameters.relax.shape
    massager = ParametersMassage(None, init_general_parameters)
    parameters = massager.parameters
    assert parameters.isif == 2


def test_relax_parameters_shape(init_general_parameters):
    del init_general_parameters.relax.volume
    del init_general_parameters.relax.positions
    massager = ParametersMassage(None, init_general_parameters)
    parameters = massager.parameters
    assert parameters.isif == 5


def test_relax_parameters_nothing(init_general_parameters):
    del init_general_parameters.relax.volume
    del init_general_parameters.relax.positions
    del init_general_parameters.relax.shape
    massager = ParametersMassage(None, init_general_parameters)
    parameters = massager.parameters
    assert parameters == AttributeDict()


def test_relax_parameters_override_isif(init_general_parameters):
    value = 1
    init_general_parameters.isif = value
    massager = ParametersMassage(None, init_general_parameters)
    parameters = massager.parameters
    assert parameters.isif == value
