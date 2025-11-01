
from sit_simulation.states.base_state import InsectState
from sit_simulation.states.dead_state import DeadState
from sit_simulation.states.pupa_state import PupaState

class LarvaState(InsectState):
    def transition(self, insect: 'Insect') -> None:
        if insect.config.larva_survive():
            insect.set_state(PupaState())
        else:
            insect.set_state(DeadState())

    def on_enter(self, insect: 'Insect') -> None:
        """Called when entering this state."""
        insect.duration = insect.config.larva_duration()