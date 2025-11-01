from sit_simulation.core.constants import StateNames
from sit_simulation.states.base_state import InsectState
from sit_simulation.states.egg_state import EggState
from sit_simulation.states.fertile_female_state import FertileFemaleState
from sit_simulation.states.larva_state import LarvaState
from sit_simulation.states.mated_female_state import MatedFemaleState
from sit_simulation.states.pupa_state import PupaState
from sit_simulation.states.sterile_female_state import SterileFemaleState
from sit_simulation.states.sterile_male_state import SterileMaleState
from sit_simulation.states.wild_male_state import WildMaleState
from sit_simulation.states.young_female_state import YoungFemaleState


class StateFactory:

    @staticmethod
    def create_state(state_type: StateNames) -> InsectState:
        match state_type:
            case StateNames.EGG:
                return EggState()
            case StateNames.LARVA:
                return LarvaState()
            case StateNames.PUPA:
                return PupaState()
            case StateNames.WM:  # Changed from MALE to WM
                return WildMaleState()
            case StateNames.SM:  # Added missing sterile male case
                return SterileMaleState()
            case StateNames.YF:
                return YoungFemaleState()
            case StateNames.FF:
                return FertileFemaleState()
            case StateNames.MF:  # Added missing mated female case
                return MatedFemaleState()
            case StateNames.SF:
                return SterileFemaleState()
            case _:
                raise ValueError(f"Unknown state type: {state_type}")