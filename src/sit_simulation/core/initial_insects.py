from typing import List

import pandas as pd

from sit_simulation.agents.insect import Insect
from sit_simulation.core.config import InsectConfig
from sit_simulation.core.spatial_manager import SpatialManager


class InitialInsects:

    def __init__(
        self,
        initial_insects: pd.DataFrame,
        spatial_manager: SpatialManager,
        insect_config: InsectConfig
    ):
        self.initial_insects = initial_insects
        self.spatial_manager = spatial_manager
        self.insect_config = insect_config

    def initial_insects_list(self) -> List[Insect]:
        insects = []

        for _, row in self.initial_insects.iterrows():
            patch = int(row['Patch'])
            for state, number in row[1:].items():
                male, state_name = (
                    (x[0] == 'Male', x[1]) if len(x := state.split()) == 2
                    else ('Male' in state, state)
                )
                insects.extend([
                    Insect(
                        is_male=male,
                        state=state_name,
                        patch=patch,
                        spatial_manager=self.spatial_manager,
                        config=self.insect_config
                    )
                    for _ in range(number)
                ])

        return insects

    @classmethod
    def load_from_file(
        cls,
        initial_insects_path: str,
        spatial_manager: SpatialManager,
        insect_config: InsectConfig
    ) -> 'InitialInsects':
        return cls(
            initial_insects=pd.read_csv(initial_insects_path),
            spatial_manager=spatial_manager,
            insect_config=insect_config
        )