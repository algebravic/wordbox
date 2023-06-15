from pysat.solvers import SolverNames
from inspect import getmembers
from pysat.card import EncType

ENCODINGS = [EncType.bitwise, EncType.cardnetwrk, EncType.kmtotalizer,
             EncType.ladder, EncType.mtotalizer,
             EncType.pairwise, EncType.seqcounter, EncType.sortnetwrk,
             EncType.totalizer]

SPECIALIZED = [EncType.pairwise,
               EncType.ladder]

SOLVERS = ['cadical', 'glucose3', 'glucose4', 'gluecard3',
           'gluecard4', 'lingeling', 'maplechrono', 'maplecm',
           'maplesat', 'mergesat3', 'minicard', 'minisat22',
           'minisatgh']

SELECTED_SOLVERS = ['cadical', 'glucose4', 'gluecard4', 'lingeling',
           'maplechrono', 'maplecm', 'maplesat', 'mergesat3',
           'minicard', 'minisat22']

def get_solver_names():
    """ Get the names of solvers."""
    for name, _ in getmembers(SolverNames, lambda _: isinstance(_, tuple)):
        yield name