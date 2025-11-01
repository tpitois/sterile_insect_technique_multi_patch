import pandas as pd

from sit_simulation.agents.insect import Insect
from sit_simulation.core.constants import StateNames


class ReleaseStrategy:

    def __init__(self, strategy: pd.DataFrame):
        self.strategy = strategy.astype('int')

    def number_of_insects(self, day, patch):
        try:
            series = self.strategy.loc[self.strategy['day'] == day, str(patch)]
            return series.values[0]
        except:
            return 0

    def release(self, simulation: 'Simulation'):
        insects_to_release = []

        for patch in range(simulation.simulation_config.numbers_of_patches):
            insects_to_release.extend([
                Insect(
                    is_male=True,
                    state=StateNames.SM,
                    patch=patch,
                    spatial_manager=simulation.spatial_manager,
                    config=simulation.insect_config
                )
                for _ in range(
                    self.number_of_insects(simulation.current_day, patch)
                )
            ])

        return insects_to_release

    @classmethod
    def load_from_file(cls, release_strategy_path: str) -> 'ReleaseStrategy':
        return cls(pd.read_csv(release_strategy_path))