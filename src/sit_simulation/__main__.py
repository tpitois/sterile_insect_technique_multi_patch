import argparse
from typing import List

from sit_simulation.core.config import SimulationConfig, InsectConfig
from sit_simulation.core.initial_insects import InitialInsects
from sit_simulation.core.release_strategy import ReleaseStrategy
from sit_simulation.core.simulation import Simulation
from sit_simulation.core.spatial_manager import SpatialManager
from sit_simulation.observers.data_collector import DataCollector
from sit_simulation.observers.logger import Logger


def main(cli_args: List[str] = None, tqdm_disable: bool = False) -> None:
    parser = argparse.ArgumentParser(description="SIT Multi-Agent Simulation")

    parser.add_argument(
        "--simu_config",
        "-sc",
        type=str,
        default="config/simulation_config.yaml",
        help="Simulation configuration file path"
    )

    parser.add_argument(
        "--insect_config",
        "-ic",
        type=str,
        default="config/insect_config.yaml",
        help="Insect configuration file path"
    )

    parser.add_argument(
        "--initial_insects",
        "-ii",
        type=str,
        default="config/initial_insects.csv",
        help="Path to initial insect folders"
    )

    parser.add_argument(
        "--release_strategy",
        "-rs",
        type=str,
        default="config/release_strategy.csv",
        help="Release strategy file path"
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="output",
        help="Path to output file"
    )

    args = parser.parse_args(cli_args)

    insect_config = InsectConfig.load_from_file(args.insect_config)
    simulation_config = SimulationConfig.load_from_file(args.simu_config)
    release_strategy = ReleaseStrategy.load_from_file(args.release_strategy)
    spatial_manager = SpatialManager(insect_config, simulation_config)
    data_collector = DataCollector(args.output)
    logger = Logger()

    initial_insects = InitialInsects.load_from_file(
        initial_insects_path=args.initial_insects,
        spatial_manager=spatial_manager,
        insect_config=insect_config,
    )

    simulation = Simulation(
        insect_config=insect_config,
        simulation_config=simulation_config,
        release_strategy=release_strategy,
        spatial_manager=spatial_manager,
        initial_insects=initial_insects.initial_insects_list(),
        observers=[data_collector, ],
    )

    simulation.run(tqdm_disable)

if __name__ == "__main__":
    main()