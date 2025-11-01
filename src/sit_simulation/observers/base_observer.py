from abc import ABC, abstractmethod



class SimulationObserver(ABC):

    @abstractmethod
    def update(self, simulation: 'Simulation') -> None:
        pass

    @abstractmethod
    def on_exit(self, simulation: 'Simulation') -> None:
        pass

    @abstractmethod
    def on_enter(self, simulation: 'Simulation') -> None:
        pass