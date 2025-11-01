
from sit_simulation.states.base_state import InsectState
from sit_simulation.states.dead_state import DeadState

class SterileFemaleState(InsectState):
    def transition(self, insect: 'Insect') -> None:
        insect.set_state(DeadState())

    def on_enter(self, insect: 'Insect') -> None:
        return