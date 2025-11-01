from typing import List

from sit_simulation.core.config import InsectConfig
from sit_simulation.core.constants import StateNames
from sit_simulation.core.spatial_manager import SpatialManager
from sit_simulation.states.base_state import InsectState
from sit_simulation.states.state_factory import StateFactory


class Insect:

    def __init__(
            self,
            is_male: bool,
            state: StateNames,
            patch: int,
            spatial_manager: SpatialManager,
            config: InsectConfig
    ):
        self.is_male = is_male
        self.state = StateFactory.create_state(state)
        self.patch = patch
        self.spatial_manager = spatial_manager
        self.config = config
        self.age = 0
        self.duration = 0
        self.next_cycle = 0
        self.nb_cycles = 0

        self.spatial_manager.init_insect(self)

        self.state.on_enter(self)

    def set_state(self, new_state: InsectState) -> None:
        if self.state:
            self.state.on_exit(self)

        old_state = self.state
        self.state = new_state
        self.age = 0

        self.spatial_manager.update_insect_state(self, old_state, new_state)

        self.state.on_enter(self)

    def update(self) -> None:
        if self.state:
            self.state.update(self)

    def reproduce(self) -> List['Insect']:
        return self.state.get_offspring(self)

    def __str__(self) -> str:
        return (
            f"Insect(state={self.state.state_name}, patch={self.patch}, "
            f"age={self.age})"
        )

    def __repr__(self) -> str:
        return (
            f"Insect(state={self.state.state_name}, patch={self.patch}, "
            f"age={self.age})"
        )
