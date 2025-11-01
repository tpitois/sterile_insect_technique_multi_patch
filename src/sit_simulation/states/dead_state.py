from sit_simulation.states.base_state import InsectState

class DeadState(InsectState):
    def update(self, insect: 'Insect') -> None:
        return

    def transition(self, insect: 'Insect') -> None:
        return

    def on_enter(self, insect: 'Insect') -> None:
        return