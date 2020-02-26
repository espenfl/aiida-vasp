"""
Representation of different containers for parameters.

------------------------------------------------------
For instance AiiDA related parameters for relaxation workflows
"""
# pylint: disable=abstract-method
# explanation: pylint wrongly complains about (aiida) Node not implementing query
from aiida.orm import Data
from plumpy import InputPort
from aiida.engine.processes.ports import PortNamespace
from aiida.engine.processes.builder import ProcessBuilderNamespace


class RelaxParameters(Data):

    _schema = PortNamespace()

    @classmethod
    def spec(cls):
        cls._schema['relax.perform'] = InputPort('relax.perform',
                                                 valid_type=get_data_class('bool'),
                                                 required=False,
                                                 default=get_data_node('bool', False),
                                                 help="""
                                                 If True, perform relaxation.
                                                 """)
        cls._schema['relax.algo'] = InputPort('relax.algo',
                                              valid_type=get_data_class('str'),
                                              default=get_data_node('str', 'cg'),
                                              help="""
                                              The algorithm to use during relaxation.
                                              """)
        cls._schema['relax.energy_cutoff'] = InputPort('relax.energy_cutoff',
                                                       valid_type=get_data_class('float'),
                                                       required=False,
                                                       help="""
                                                       The cutoff that determines when the relaxation procedure is stopped. In this
                                                       case it stops when the total energy between two ionic steps is less than the
                                                       supplied value.
                                                       """)
        cls._schema['relax.force_cutoff'] = InputPort('relax.force_cutoff',
                                                      valid_type=get_data_class('float'),
                                                      required=False,
                                                      help="""
                                                      The cutoff that determines when the relaxation procedure is stopped. In this
                                                      case it stops when all forces are smaller than than the
                                                      supplied value.
                                                      """)
        cls._schema['relax.steps'] = InputPort('relax.steps',
                                               valid_type=get_data_class('int'),
                                               required=False,
                                               default=get_data_node('int', 60),
                                               help="""
                                               The number of relaxation steps to perform (updates to the atomic positions,
                                               unit cell size or shape).
                                               """)
        cls._schema['relax.positions'] = InputPort('relax.positions',
                                                   valid_type=get_data_class('bool'),
                                                   required=False,
                                                   default=get_data_node('bool', True),
                                                   help="""
                                                   If True, perform relaxation of the atomic positions.
                                                   """)
        cls._schema['relax.shape'] = InputPort('relax.shape',
                                               valid_type=get_data_class('bool'),
                                               required=False,
                                               default=get_data_node('bool', False),
                                               help="""
                                               If True, perform relaxation of the unit cell shape.
                                               """)
        cls._schema['relax.volume'] = InputPort('relax.volume',
                                                valid_type=get_data_class('bool'),
                                                required=False,
                                                default=get_data_node('bool', False),
                                                help="""
                                                If True, perform relaxation of the unit cell volume..
                                                """)
        cls._schema['relax.convergence_on'] = InputPort('relax.convergence_on',
                                                        valid_type=get_data_class('bool'),
                                                        required=False,
                                                        default=get_data_node('bool', False),
                                                        help="""
                                                        If True, test convergence based on selected criterias set.
                                                        """)
        cls._schema['relax.convergence_absolute'] = InputPort('relax.convergence_absolute',
                                                              valid_type=get_data_class('bool'),
                                                              required=False,
                                                              default=get_data_node('bool', False),
                                                              help="""
                                                              If True, test convergence based on absolute differences.
                                                              """)
        cls._schema['relax.convergence_max_iterations'] = InputPort('relax.convergence_max_iterations',
                                                                    valid_type=get_data_class('int'),
                                                                    required=False,
                                                                    default=get_data_node('int', 5),
                                                                    help="""
                                                                    The number of iterations to perform if the convergence criteria is not met.
                                                                    """)
        cls._schema['relax.convergence_volume'] = InputPort('relax.convergence_volume',
                                                            valid_type=get_data_class('float'),
                                                            required=False,
                                                            default=get_data_node('float', 0.01),
                                                            help="""
                                                            The cutoff value for the convergence check on volume. If ``convergence_absolute``
                                                            is True in AA, otherwise in relative.
                                                            """)
        cls._schema['relax.convergence_positions'] = InputPort('relax.convergence_positions',
                                                               valid_type=get_data_class('float'),
                                                               required=False,
                                                               default=get_data_node('float', 0.01),
                                                               help="""
                                                               The cutoff value for the convergence check on positions. If ``convergence_absolute``
                                                               is True in AA, otherwise in relative difference.
                                                               """)
        cls._schema['relax.convergence_shape_lengths'] = InputPort('relax.convergence_shape_lengths',
                                                                   valid_type=get_data_class('float'),
                                                                   required=False,
                                                                   default=get_data_node('float', 0.1),
                                                                   help="""
                                                                   The cutoff value for the convergence check on the lengths of the unit cell
                                                                   vecotrs. If ``convergence_absolute``
                                                                   is True in AA, otherwise in relative difference.
                                                                   """)
        cls._schema['relax.convergence_shape_angles'] = InputPort('relax.convergence_shape_angles',
                                                                  valid_type=get_data_class('float'),
                                                                  required=False,
                                                                  default=get_data_node('float', 0.1),
                                                                  help="""
                                                                  The cutoff value for the convergence check on the angles of the unit cell.
                                                                  If ``convergence_absolute`` is True in degrees, otherwise in relative difference.
                                                                  """)

        return cls._schema

    @classmethod
    def get_builder(cls):
        return ProcessBuilderNamespace(cls.spec())
