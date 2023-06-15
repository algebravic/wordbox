"""
Run a bunch of experiments.
"""

import argparse
from itertools import islice
from sacred.observers import FileStorageObserver, MongoObserver, TinyDbObserver
from itertools import product
from threading import Timer
from pysat.card import EncType
from .experiments import ex
from .configurations import get_configs, good_problems
from pathlib import Path
from .solve_glue import DATADIR

FILE_OBSERVER = DATADIR / 'wordbox'

# ex.observers.append(MongoObserver(db_name='wordbox'))
# ex.observers.append(TinyDbObserver(path='../data/wordbox'))
ex.observers.append(FileStorageObserver(FILE_OBSERVER))

def run_solvers(mval, nval, wordlist, time_limit=-1.0, start=0, rerun=False):
    for config in good_problems(FILE_OBSERVER, mval, nval, wordlist, time_limit=time_limit, start=start, rerun=rerun):
        ex.run(config_updates=config)
        
def main():
    parser = argparse.ArgumentParser(description="Wordbox Problem")
    parser.add_argument('mval', type=int, default=5,
                        help='The width of the wordbox')
    
    parser.add_argument('nval', type=int, default=7,
                        help='The height of the wordbox')

    parser.add_argument('--time_limit', type=float, default=-1.0,
                        help='A time limit for a solver')

    parser.add_argument('--start', type=int, default=0,
                        help='Starting point for running problems')

    parser.add_argument('--wordlist', type=str, default='planets',
                        help='The name of the word list to use')

    parser.add_argument('--rerun', type=bool, default=False,
                        help='Should we rerun previously completed instances?')

    args = parser.parse_args()
    run_solvers(args.mval, args.nval, args.wordlist, time_limit=args.time_limit, start=args.start, rerun=args.rerun)

if __name__ == '__main__':
    main()
    
