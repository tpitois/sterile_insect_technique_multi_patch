from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

from sit_simulation.core.constants import ADULT_STATES

if TYPE_CHECKING:
    from sit_simulation.agents.insect import Insect


class InsectState(ABC):
    """Base class for all insect states."""

    def update(self, insect: 'Insect') -> None:
        if self.state_name in ADULT_STATES:
            insect.spatial_manager.update_insect_patch(insect)
        insect.age += 1
        if insect.age > insect.duration:
            self.transition(insect)

    @abstractmethod
    def transition(self, insect: 'Insect') -> None:
        """Check and perform state transition if conditions are met."""
        pass

    @abstractmethod
    def on_enter(self, insect: 'Insect') -> None:
        """Called when entering this state."""
        pass

    def on_exit(self, insect: 'Insect') -> None:
        """Called when exiting this state."""
        pass

    def get_offspring(self, insect: 'Insect') -> List['Insect']:
        return []

    @property
    def state_name(self) -> str:
        """Return the name of this state."""
        return self.__class__.__name__.replace('State', '')