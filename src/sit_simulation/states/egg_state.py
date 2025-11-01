from sit_simulation.states.base_state import InsectState
from sit_simulation.states.dead_state import DeadState
from sit_simulation.states.larva_state import LarvaState


class EggState(InsectState):
    def transition(self, insect: 'Insect') -> None:
        if insect.config.egg_survive():
            insect.set_state(LarvaState())
        else:
            insect.set_state(DeadState())

    def on_enter(self, insect: 'Insect') -> None:
        insect.duration = insect.config.egg_duration()
