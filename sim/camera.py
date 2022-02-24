from dataclasses import dataclass
from typing import List, Set
from person import Person
from publisher import Publisher
import json


@dataclass
class Camera:
    threshold: float
    publisher: Publisher
    up: int = 0
    down: int = 0
    counted_people = set()
    frame: int = 0

    def send_message(self, people: List[Person]):
        for person in people:
            if person in self.counted_people:
                continue
            if person.position > self.threshold and person.speed > 0:
                self.up += 1
                self.counted_people.add(person)
            elif person.position < self.threshold and person.speed < 0:
                self.down += 1
                self.counted_people.add(person)

        self.frame += 1

        data = {
            "totalFrames": self.frame,
            "totalDetected": self.up + self.down,
            "totalEnter": self.up,
            "totalExit": self.down,
            "totalInRoom": self.down - self.up,
        }

        self.publisher.publish(json.dumps(data))
