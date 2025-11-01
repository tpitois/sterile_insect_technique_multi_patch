import logging
import sys

from sit_simulation.core.simulation import Simulation
from sit_simulation.observers.base_observer import SimulationObserver


class Logger(SimulationObserver):
    def __init__(self) -> None:
        self.logger = logging.getLogger("Logger")
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler(sys.stdout))

    def update(self, simulation: Simulation) -> None:
        self.logger.info(
            f"Day {simulation.current_day}"
            f"/{simulation.simulation_config.numbers_of_day}"
        )

    def on_exit(self, simulation: Simulation) -> None:
        self.logger.info("Simulation finished")

    def on_enter(self, simulation: Simulation) -> None:
        self.logger.info("Simulation started")
