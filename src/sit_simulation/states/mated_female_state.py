from typing import List

from sit_simulation.core.constants import StateNames
from sit_simulation.states.base_state import InsectState
from sit_simulation.states.dead_state import DeadState


class MatedFemaleState(InsectState):
    def transition(self, insect: 'Insect') -> None:
        insect.set_state(DeadState())

    def on_enter(self, insect: 'Insect') -> None:
        """Called when entering this state."""
        insect.duration += insect.config.female_lifespan()
        insect.next_cycle = insect.age + insect.config.female_mate_next_cycle()

    def get_offspring(self, insect: 'Insect') -> List['Insect']:
        from sit_simulation.agents.insect import Insect
        if (insect.age >= insect.next_cycle
        and insect.nb_cycles <= insect.config.female_max_mating_cycles
        ):
            nb_male_eggs, nb_female_eggs = (
                insect.spatial_manager.numbers_of_eggs(insect)
            )

            offspring = (
                [
                    Insect(
                        is_male=True,
                        state=StateNames.EGG,
                        patch=insect.patch,
                        spatial_manager=insect.spatial_manager,
                        config=insect.config
                    )
                    for _ in range(nb_male_eggs)
                ]
                + [
                    Insect(
                        is_male=False,
                        state=StateNames.EGG,
                        patch=insect.patch,
                        spatial_manager=insect.spatial_manager,
                        config=insect.config
                    )
                    for _ in range(nb_female_eggs)
                ]
            )

            insect.next_cycle = insect.age + insect.config.female_mate_next_cycle()

            return offspring
        return []