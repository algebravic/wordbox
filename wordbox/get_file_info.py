"""
Get information from a file observer
"""
import json
from pathlib import Path

def info(filepath):
    """ Information from an experiment directory """
    obs_dir = Path(filepath)

    for run_dir in obs_dir.glob('*'):
        serial = run_dir.name
        if not serial.isnumeric():
            continue
        try:
            with (run_dir / 'config.json').open() as fil:
                config = json.load(fil)
        except FileNotFoundError:
            print(f"Entry {serial} has no config, skipping")
            continue

        try:
            with (run_dir / 'cout.txt').open() as fil:
                cout = fil.read()
        except FileNotFoundError:
            cout = None

        try:
            with (run_dir / 'metrics.json').open() as fil:
                metrics = json.load(fil)
        except FileNotFoundError:
            metrics = None

        try:
            with (run_dir / 'run.json').open() as fil:
                run = json.load(fil)
        except FileNotFoundError:
            run = {"status":"MISSING"}

        run.update(
            serial=serial,
            config=config,
            captured_out=cout,
            metrics=metrics
        )
        yield run

def completed(filepath):
    """
    The set of completed runs.
    """
    good = set()
    for run in info(filepath):
        if run['status'] == 'COMPLETED':
            config = run['config'].copy()
            if 'seed' in config:
                del config['seed']
            if 'time_limit' in config:
                del config['time_limit']
            good.add(tuple(sorted(config.items())))
    return good
