
from sit_simulation.states.base_state import InsectState
from sit_simulation.states.dead_state import DeadState
from sit_simulation.states.wild_male_state import WildMaleState
from sit_simulation.states.young_female_state import YoungFemaleState

class PupaState(InsectState):
    def transition(self, insect: 'Insect') -> None:
        if insect.config.pupa_survive():
            if insect.is_male:
                insect.set_state(YoungFemaleState())
            else:
                insect.set_state(WildMaleState())
        else:
            insect.set_state(DeadState())

    def on_enter(self, insect: 'Insect') -> None:
        """Called when entering this state."""
        insect.duration = insect.config.pupa_duration()