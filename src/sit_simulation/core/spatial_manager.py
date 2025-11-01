import random
from collections import defaultdict

import numpy as np

from sit_simulation.core.config import SimulationConfig, InsectConfig
from sit_simulation.core.constants import StateNames
from sit_simulation.states.base_state import InsectState


class SpatialManager:

    def __init__(
            self,
            insect_config: InsectConfig,
            simulation_config: SimulationConfig
    ) -> None:
        self.insect_config = insect_config
        self.simulation_config = simulation_config
        self.cdf_migration_rates = np.cumsum(
            self.simulation_config.migration_rates, axis=1
        )
        self.numbers_of_insects = [
            defaultdict(int)
            for _ in range(self.simulation_config.numbers_of_patches)
        ]

    def update_insect_state(self, insect: 'Insect', old_state: InsectState, new_state: InsectState):
        self.numbers_of_insects[insect.patch][old_state.state_name] += -1
        self.numbers_of_insects[insect.patch][new_state.state_name] += 1

    def update_insect_patch(self, insect: 'Insect'):
        if insect.state.state_name in [StateNames.EGG, StateNames.LARVA, StateNames.PUPA]:
            return

        new_patch = self._random_patch(insect.patch)
        self.numbers_of_insects[insect.patch][insect.state.state_name] += -1
        self.numbers_of_insects[new_patch][insect.state.state_name] += 1
        insect.patch = new_patch


    def mate_occurs(self, insect: 'Insect'):
        """
        :param insect:
        :return: return 0 if nothing happened, 1 if mate is fertile and -1 if is sterile
        """
        if random.random() >= self.simulation_config.mating_rates[insect.patch]:
            return 0

        wm_number = self.numbers_of_insects[insect.patch][StateNames.WM]
        sm_number = self.numbers_of_insects[insect.patch][StateNames.SM]
        competitiveness = self.insect_config.sterile_male_competitiveness

        is_fertile = (
                random.uniform(0, wm_number + competitiveness * sm_number)
                < wm_number
        )

        return 2 * is_fertile - 1


    def numbers_of_eggs(self, insect: 'Insect'):
        """

        :param insect:
        :return: nb_male_eggs, nb_female_eggs
        """
        max_eggs = max(
            0,
            (
                self.simulation_config.capacities[insect.patch]
                - self.numbers_of_insects[insect.patch][StateNames.EGG]
            )
        )

        nb_male_eggs = insect.config.eggs_male_count()
        nb_female_eggs = insect.config.eggs_female_count()

        k = min(max_eggs / (nb_male_eggs + nb_female_eggs), 1)

        nb_male_eggs *= k
        nb_female_eggs *= k

        return int(nb_male_eggs), int(nb_female_eggs)

    def _random_patch(self, patch):
        new_patch = 0
        r = random.random()
        while self.cdf_migration_rates[patch][new_patch] < r:
            new_patch += 1
        return new_patch

    def init_insect(self, insect: 'Insect'):
        self.numbers_of_insects[insect.patch][insect.state.state_name] += 1
