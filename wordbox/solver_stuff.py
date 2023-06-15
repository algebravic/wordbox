""" Definitions for solvers and cardinality constraints """
from inspect import getmembers
from pysat.solvers import SolverNames
from pysat.card import EncType

ENCODINGS = [EncType.bitwise, EncType.cardnetwrk, EncType.kmtotalizer,
             EncType.ladder, EncType.mtotalizer,
             EncType.pairwise, EncType.seqcounter, EncType.sortnetwrk,
             EncType.totalizer]

SPECIALIZED = [EncType.pairwise,
               EncType.ladder]

SOLVERS = ['cadical153', 'cadical103', 'glucose3', 'glucose4', 'gluecard3',
           'gluecard4', 'lingeling', 'maplechrono', 'maplecm',
           'maplesat', 'mergesat3', 'minicard', 'minisat22',
           'minisatgh']

SELECTED_SOLVERS = ['cadical153', 'glucose4', 'gluecard4', 'lingeling',
           'maplechrono', 'maplecm', 'maplesat', 'mergesat3',
           'minicard', 'minisat22']

def get_solver_names():
    """ Get the names of solvers."""
    for name, _ in getmembers(SolverNames, lambda _: isinstance(_, tuple)):
        yield name
