import argparse
import os

from pathlib import Path
from typing import List

import numpy as np
import pandas as pd

from sit_simulation.core.config import SimulationConfig
from sit_simulation.core.constants import StateNames


def process_simulation(
        data_simulation: List[pd.DataFrame],
        release_strategy: pd.DataFrame,
        past_len: int,
        future_len: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    data_simulation = [
        df[
            sorted([col for col in df.columns if col != StateNames.SM])
            + [StateNames.SM]
        ].drop(columns=['Day']).values
        for df in data_simulation
    ]
    simulation = np.concatenate(data_simulation, axis=1)

    strat = np.zeros((future_len, len(release_strategy.columns) - 1))

    for i in range(strat.shape[0]):
        strat[i, :] = release_strategy[release_strategy['day']==76].values[0, 1:]

    return (
        simulation[:past_len, :],
        simulation[past_len:past_len+future_len, :],
        strat
    )

def process_dataset(
        dataset_path: Path,
        simulation_config: SimulationConfig,
        past_len: int,
        future_len: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    dataset = [
        [
            [
                pd.read_csv(dataset_path / dir_name / f'patch_{patch}.csv')
                for patch in range(simulation_config.numbers_of_patches)
            ],
            pd.read_csv(dataset_path / dir_name / 'release_strategy.csv')[['day']+[str(x) for x in range(simulation_config.numbers_of_patches)]]
        ]
        for dir_name in next(os.walk(dataset_path))[1]
    ]

    past_list, future_list, release_strategy_list = zip(*[
        process_simulation(*(simulation + [past_len, future_len]))
        for simulation in dataset
    ])

    return (
        np.array(past_list),
        np.array(future_list),
        np.array(release_strategy_list),
    )

def main():
    parser = argparse.ArgumentParser(description="SIT Multi-Agent Simulation")

    parser.add_argument(
        "--simu_config",
        "-sc",
        type=str,
        default="config/simulation_config.yaml",
        help="Simulation configuration file path"
    )

    parser.add_argument(
        "--input",
        "-i",
        type=str,
        default="input",
        help="Path to input folder"
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="output",
        help="Path to output folder"
    )

    parser.add_argument(
        "--past_len",
        type=int,
        default=20,
        help="Past length of simulation"
    )

    parser.add_argument(
        "--future_len",
        type=int,
        default=80,
        help="Future length of simulation"
    )


    args = parser.parse_args()

    simulation_config = SimulationConfig.load_from_file(args.simu_config)

    past, future, release_strategy = process_dataset(
        Path(args.input),
        simulation_config,
        past_len=args.past_len,
        future_len=args.future_len,
    )

    os.makedirs(Path(args.output), exist_ok=True)

    np.save(Path(args.output) / 'past.npy', past)
    np.save(Path(args.output) / 'future.npy', future)
    np.save(Path(args.output) / 'release_strategy.npy', release_strategy)

if __name__ == "__main__":
    main()
