
from sit_simulation.states.base_state import InsectState
from sit_simulation.states.fertile_female_state import FertileFemaleState


class YoungFemaleState(InsectState):
    def transition(self, insect: 'Insect') -> None:
        insect.set_state(FertileFemaleState())

    def on_enter(self, insect: 'Insect') -> None:
        """Called when entering this state."""
        insect.duration = insect.config.female_first_blood_meal()

    def on_exit(self, insect: 'Insect') -> None:
        insect.duration += - insect.age