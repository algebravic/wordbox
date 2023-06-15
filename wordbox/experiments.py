"""
Use sacred to run experiments.
"""

from sacred import Experiment
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from time import sleep
from sacred.utils import TimeoutInterrupt
from .solve_glue import run_solver

ex = Experiment('Word Box')

@ex.config
def wordbox_config():

    mval = 5
    nval = 7
    wordlist = 'planets'
    solver = 'cadical'
    coloring = True
    bip = True
    cardinality = -1 # No extra cardinality constraints
    time_limit = -1.0 # no limit

@ex.main
def solveit(mval, nval, wordlist, solver, coloring, bip, cardinality, time_limit):

    if time_limit < 0:
        return run_solver(mval, nval, wordlist, solver, coloring, bip, cardinality)
        
    print("Using time limit {}".format(time_limit))
    with ThreadPoolExecutor(2) as excecutor:
        future = excecutor.submit(run_solver, mval, nval, wordlist, solver, coloring, bip, cardinality, time_limit=time_limit)
    try:
        return future.result(timeout=time_limit)
    except TimeoutError:
        raise TimeoutInterrupt()

def run_main():
    ex.run_commandline()

if __name__ == '__main__':
    run_main()
    
