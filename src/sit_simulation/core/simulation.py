from typing import List

from tqdm import tqdm

from sit_simulation.agents.insect import Insect
from sit_simulation.core.config import SimulationConfig, InsectConfig
from sit_simulation.core.constants import StateNames
from sit_simulation.core.insect_manager import InsectManager
from sit_simulation.core.release_strategy import ReleaseStrategy
from sit_simulation.core.spatial_manager import SpatialManager
from sit_simulation.observers.base_observer import SimulationObserver


class Simulation:

    def __init__(
            self,
            insect_config: InsectConfig,
            simulation_config: SimulationConfig,
            release_strategy: ReleaseStrategy,
            spatial_manager: SpatialManager,
            initial_insects: List[Insect],
            observers: List[SimulationObserver]
    ):
        self.insect_config = insect_config
        self.simulation_config = simulation_config
        self.release_strategy = release_strategy
        self.spatial_manager = spatial_manager
        self.insect_manager = InsectManager(initial_insects)
        self.observers = observers
        self.current_day = 0

    def update(self):
        self.current_day += 1

        while not self.insect_manager.is_empty():
            insect = self.insect_manager.pop()
            insect.update()

            if insect.state.state_name == StateNames.DEAD:
                continue

            self.insect_manager.extend(insect.reproduce())
            self.insect_manager.append(insect)

        self.insect_manager.extend(self.release_strategy.release(self))
        self.insect_manager.update()

        for observer in self.observers:
            observer.update(self)

    def run(self, tqdm_disable: bool = False):
        for observer in self.observers:
            observer.on_enter(self)

        for _ in tqdm(range(self.simulation_config.numbers_of_day), disable=tqdm_disable):
            self.update()

        for observer in self.observers:
            observer.on_exit(self)



