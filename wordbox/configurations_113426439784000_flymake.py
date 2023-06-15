"""
The list of parameters to run for a particular wordbox instance
"""
from itertools import product, islice
from .solver_stuff import ENCODINGS, SELECTED_SOLVERS, SPECIALIZED
from pysat.card import EncType
from .get_file_info import completed

def get_configs():
    """ Return the configurations."""
    general_encodings = tuple(sorted(set(ENCODINGS).difference(SPECIALIZED)))
    config = {}
    for solver in SELECTED_SOLVERS:
        config['solver'] = solver
        for bip, coloring in  product((False, True), repeat=2):
            config['bip'] = bip
            config['coloring'] = coloring
            color_code = general_encodings if coloring else ()
            generals = (-1, ) + color_code
            encodings = ( (EncType.native, ) if 'card' in solver else generals)
            for encoding in encodings:
                config['cardinality'] = encoding
                yield config.copy() # it is important to copy here!


def good_problems(file_observer, mval, nval, wordlist,
                  time_limit=-1.0, start=0, rerun=False):
    myruns = completed(file_observer)
    for config in islice(get_configs(), start, None):
        config.update(
            {"mval":mval, "nval":nval, "wordlist":wordlist, "time_limit":time_limit})
        if not rerun:
            cconfig = config.copy()
            if 'time_limit' in cconfig:
                del cconfig['time_limit']
            tconfig = tuple(sorted(cconfig.items()))
            if tconfig in myruns:
                print(f"Already ran {config}")
                continue
        yield config
