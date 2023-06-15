""" Glue functions for sacred """
from pathlib import Path
import argparse
from homomorphism import problem, LISTS
from . import __path__ as modpath

# DATADIR = Path('~/Programming/SAT/wordbox/data/CNF').expanduser()
# Make the DATADIR relative to the this package
DATADIR = (Path(modpath[0]) / '../data').resolve()


def get_model(mval, nval, wordlist, coloring, bip, cardinality):
    """ Get the model from homomorphism """
    prob = problem(mval, nval, wordlist=LISTS[wordlist])
    return prob.model(coloring=coloring, bip=bip, cardinality=cardinality)

def run_solver(mval, nval, wordlist,
               solver, coloring, bip,
               cardinality, time_limit=-1.0):
    """ Run the solver for the constructed model """
    print(f"Running({mval}, {nval}, {wordlist}, solver={solver}, "
          + f"coloring={coloring}, bip={bip}, cardinality={cardinality}")

    mod = get_model(mval, nval, wordlist, coloring, bip, cardinality)
    mod.solve(solver=solver, time_limit=time_limit)
    if mod._status:
        values = mod.check()
    else:
        values = dict()
    return mod._solveit.accum_stats(), mod.solve_time, values

def make_cnf(datadir=DATADIR):
    """ Produce CNF for the constructed model """
    parser = argparse.ArgumentParser(description="Wordbox Problem")
    parser.add_argument('mval', type=int, default=5,
                        help='The width of the wordbox')
    parser.add_argument('nval', type=int, default=7,
                        help='The height of the wordbox')

    parser.add_argument('--wordlist', type=str, default='planets',
                        help='The name of the word list to use')

    parser.add_argument('--bip', type=bool, default=False,
                        help='Use bipartite constraints')

    parser.add_argument('--coloring', type=bool, default=False,
                        help='Use coloring constraints')

    parser.add_argument('--cardinality', type=int, default=-1,
                        help='Encode extra cardinality constraints constraints')

    args = parser.parse_args()
    mod = get_model(args.mval, args.nval, args.wordlist, args.coloring, args.bip, args.cardinality)
    # Now make up the name
    card_str = int(args.cardinality) if args.cardinality >=0 else ''
    name = (f'wordbox_{args.mval}_{args.nval}_{int(args.bip)}'
            + f'_{int(args.coloring)}'
            + f'_{card_str}.cnf')

    mod._cnf.to_file((datadir / 'CNF') / name)
