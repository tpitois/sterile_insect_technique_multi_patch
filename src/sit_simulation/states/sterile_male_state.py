
from sit_simulation.states.base_state import InsectState
from sit_simulation.states.dead_state import DeadState


class SterileMaleState(InsectState):
    def transition(self, insect: 'Insect') -> None:
        insect.set_state(DeadState())

    def on_enter(self, insect: 'Insect') -> None:
        """Called when entering this state."""
        insect.duration = insect.config.sterile_male_lifespan()