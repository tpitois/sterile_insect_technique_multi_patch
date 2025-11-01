
from sit_simulation.states.base_state import InsectState
from sit_simulation.states.dead_state import DeadState
from sit_simulation.states.mated_female_state import MatedFemaleState
from sit_simulation.states.sterile_female_state import SterileFemaleState


class FertileFemaleState(InsectState):
    def update(self, insect: 'Insect') -> None:
        insect.spatial_manager.update_insect_patch(insect)
        insect.age += 1
        if insect.age > insect.duration:
            self.transition(insect)
        mate = insect.spatial_manager.mate_occurs(insect)
        if mate == 1:
            insect.set_state(MatedFemaleState())
        elif mate == -1:
            insect.set_state(SterileFemaleState())

    def transition(self, insect: 'Insect') -> None:
        insect.set_state(DeadState())

    def on_enter(self, insect: 'Insect') -> None:
        """Called when entering this state."""
        insect.duration += insect.config.female_lifespan()

    def on_exit(self, insect: 'Insect') -> None:
        insect.duration += - insect.age