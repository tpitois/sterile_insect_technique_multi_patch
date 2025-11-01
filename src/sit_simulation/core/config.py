from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, List
from typing import Tuple

import numpy as np
import yaml

from sit_simulation.core.constants import ProbabilityDistribution


@dataclass
class InsectConfig:
    # Egg stage configuration
    egg_duration_dist: ProbabilityDistribution = ProbabilityDistribution.UNIFORM
    egg_duration_param: Tuple[float, ...] = (4.5, 0.7)
    egg_survive_dist: ProbabilityDistribution = ProbabilityDistribution.BERNOULLI
    egg_survive_param: Tuple[float, ...] = (0.492,)

    # Larva stage configuration
    larva_duration_dist: ProbabilityDistribution = ProbabilityDistribution.UNIFORM
    larva_duration_param: Tuple[float, ...] = (7.3, 0.6)
    larva_survive_dist: ProbabilityDistribution = ProbabilityDistribution.BERNOULLI
    larva_survive_param: Tuple[float, ...] = (0.812,)

    # Pupa stage configuration
    pupa_duration_dist: ProbabilityDistribution = ProbabilityDistribution.UNIFORM
    pupa_duration_param: Tuple[float, ...] = (2.7, 0.1)
    pupa_survive_dist: ProbabilityDistribution = ProbabilityDistribution.BERNOULLI
    pupa_survive_param: Tuple[float, ...] = (0.938,)

    # Male adult configuration
    wild_male_lifespan_dist: ProbabilityDistribution = ProbabilityDistribution.WEIBULL
    wild_male_lifespan_param: Tuple[float, ...] = (2.1945968574915145, 22.84070720300488)

    # Sterile male adult configuration
    sterile_male_competitiveness: float = 0.5
    sterile_male_lifespan_dist: ProbabilityDistribution = ProbabilityDistribution.WEIBULL
    sterile_male_lifespan_param: Tuple[float, ...] = (2.1945968574915145, 16)

    # Female adult configuration
    female_lifespan_dist: ProbabilityDistribution = ProbabilityDistribution.WEIBULL
    female_lifespan_param: Tuple[float, ...] = (2.208137541820492, 25.482192728652816)

    # Female mating configuration
    female_mate_next_cycle_dist: ProbabilityDistribution = ProbabilityDistribution.NORMAL
    female_mate_next_cycle_param: Tuple[float, ...] = (5, 1)

    eggs_male_dist: ProbabilityDistribution = ProbabilityDistribution.NORMAL
    eggs_male_param: Tuple[float, ...] = (10, 5)

    eggs_female_dist: ProbabilityDistribution = ProbabilityDistribution.NORMAL
    eggs_female_param: Tuple[float, ...] = (9, 5)

    female_max_mating_cycles: int = 5

    # Female first blood meal configuration
    female_first_blood_dist: ProbabilityDistribution = ProbabilityDistribution.NORMAL
    female_first_blood_param: Tuple[float, ...] = (5.54, 0.82)

    @classmethod
    def egg_duration(cls) -> float:
        return cls._simulate_rv(
            cls.egg_duration_dist, cls.egg_duration_param
        )

    @classmethod
    def egg_survive(cls) -> bool:
        return cls._simulate_rv(
            cls.egg_survive_dist, cls.egg_survive_param
        )

    @classmethod
    def larva_duration(cls) -> float:
        return cls._simulate_rv(
            cls.larva_duration_dist, cls.larva_duration_param
        )

    @classmethod
    def larva_survive(cls) -> bool:
        return cls._simulate_rv(
            cls.larva_survive_dist, cls.larva_survive_param
        )

    @classmethod
    def pupa_duration(cls) -> float:
        return cls._simulate_rv(
            cls.pupa_duration_dist, cls.pupa_duration_param
        )

    @classmethod
    def pupa_survive(cls) -> bool:
        return cls._simulate_rv(
            cls.pupa_survive_dist, cls.pupa_survive_param
        )

    @classmethod
    def wild_male_lifespan(cls) -> float:
        return cls._simulate_rv(
            cls.wild_male_lifespan_dist, cls.wild_male_lifespan_param
        )

    @classmethod
    def sterile_male_lifespan(cls) -> float:
        return cls._simulate_rv(
            cls.sterile_male_lifespan_dist, cls.sterile_male_lifespan_param
        )

    @classmethod
    def female_lifespan(cls) -> float:
        return cls._simulate_rv(
            cls.female_lifespan_dist, cls.female_lifespan_param
        )

    @classmethod
    def female_mate_next_cycle(cls) -> float:
        return cls._simulate_rv(
            cls.female_mate_next_cycle_dist, cls.female_mate_next_cycle_param
        )

    @classmethod
    def eggs_male_count(cls) -> float:
        return cls._simulate_rv(
            cls.eggs_male_dist, cls.eggs_male_param
        )

    @classmethod
    def eggs_female_count(cls) -> float:
        return cls._simulate_rv(
            cls.eggs_female_dist, cls.eggs_female_param
        )

    @classmethod
    def female_first_blood_meal(cls) -> float:
        return cls._simulate_rv(
            cls.female_first_blood_dist, cls.female_first_blood_param
        )

    @staticmethod
    def _simulate_rv(distribution: ProbabilityDistribution, params):
        match distribution:
            case ProbabilityDistribution.UNIFORM:
                a = params[0]
                b = params[1]
                return (b - a) * np.random.rand() + a
            case ProbabilityDistribution.GEOM:
                return np.random.geometric(*params)
            case ProbabilityDistribution.NORMAL:
                return max(np.random.normal(*params), 0.1)
            case ProbabilityDistribution.WEIBULL:
                return params[1] * (-np.log(np.random.rand())) ** (1 / params[0])
            case ProbabilityDistribution.BERNOULLI:
                return np.random.binomial(1, params[0])
            case _:
                raise ValueError(f"Unknown distribution: {distribution}")

    @classmethod
    def load_from_file(cls, config_path: str) -> 'InsectConfig':
        path = Path(config_path)
        with open(path, 'r') as f:
            config_data = yaml.safe_load(f)
        return cls.from_dict(config_data)

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'InsectConfig':
        return cls(**config_dict)


@dataclass
class SimulationConfig:
    numbers_of_day: int = 50
    numbers_of_patches: int = 10
    migration_rates: List[List[float]] = None
    mating_rates: List[float] = None
    capacities: List[int] = None

    @classmethod
    def load_from_file(cls, config_path: str) -> 'SimulationConfig':
        path = Path(config_path)
        with open(path, 'r') as f:
            config_data = yaml.safe_load(f)
        return cls.from_dict(config_data)

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'SimulationConfig':
        return cls(**config_dict)