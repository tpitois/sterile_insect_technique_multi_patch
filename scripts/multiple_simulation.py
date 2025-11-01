import argparse
import functools
import os
import random
from typing import List

import pandas as pd
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map

from sit_simulation.__main__ import main as sit_main
from sit_simulation.core.config import SimulationConfig


def get_sit_args(base_config: str, output: str, release_strategy) -> List[str]:
    return [
        '--simu_config', base_config + '/simulation_config.yaml',
        '--insect_config',  base_config + '/insect_config.yaml',
        '--initial_insects', base_config + '/initial_insects.csv',
        '--release_strategy', release_strategy,
        '--output', output # <-- New output
    ]


def generate_release_strategy(output: str, simulation_config: SimulationConfig):
    df = pd.DataFrame(columns=['day']+list(range(simulation_config.numbers_of_patches)))
    a, b = random.uniform(0, 100000), random.uniform(0, 100000)
    for day in range(20, simulation_config.numbers_of_day, 7):
        df.loc[len(df), :] = [day, a, b]
    df.to_csv(output)

def run_sit(number, args, simulation_config: SimulationConfig):
    output = f'{args.output}/{number}'
    os.makedirs(output)
    generate_release_strategy(f'{output}/release_strategy.csv', simulation_config)
    sit_args = get_sit_args(
        base_config=args.base_config,
        output=output,
        release_strategy=f'{output}/release_strategy.csv'
    )
    sit_main(sit_args, tqdm_disable=True)

def main():
    parser = argparse.ArgumentParser(description="Execute Multiple SIT Simulation")

    parser.add_argument(
        "--base_config",
        type=str,
        default="config",
        help="Simulation base configuration folder"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="two_patches_output",
        help="Output folder"
    )

    parser.add_argument(
        "--number_of_simulations",
        type=int,
        default=1000,
        help="Number of simulations"
    )

    args = parser.parse_args()

    os.makedirs(f'{args.output}')

    simulation_config = SimulationConfig.load_from_file(
        f'{args.base_config}/simulation_config.yaml'
    )

    run_sit_partial = functools.partial(
        run_sit,
        args=args,
        simulation_config=simulation_config
    )

    results = process_map(
        run_sit_partial,
        range(0, args.number_of_simulations),
        max_workers=10
    )


if __name__ == '__main__':
    main()

