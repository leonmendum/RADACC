from dataclasses import dataclass


@dataclass
class Person:
    """Class for keeping track of a person in the simulation."""

    id: int
    position: float
    speed: float

    def update(self, time_resolution: float = 1 / 5):
        """Update the position of the person"""
        self.position += self.speed + time_resolution

    def __hash__(self) -> int:
        return self.id
