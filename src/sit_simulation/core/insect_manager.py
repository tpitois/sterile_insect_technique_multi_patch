from typing import List

from sit_simulation.agents.insect import Insect


class InsectManager:

    def __init__(self, initial_insects: List[Insect]):
        self.current_list = 0
        self.insect_lists = [[], []]
        self.insect_lists[0] = initial_insects.copy()

    def is_empty(self) -> bool:
        return not self.insect_lists[self.current_list]

    def pop(self) -> Insect:
        return self.insect_lists[self.current_list].pop()

    def append(self, insect: Insect) -> None:
        self.insect_lists[(1 + self.current_list) % 2].append(insect)

    def extend(self, insects: List[Insect]) -> None:
        self.insect_lists[(1 + self.current_list) % 2].extend(insects)

    def update(self) -> None:
        self.current_list = (1 + self.current_list) % 2