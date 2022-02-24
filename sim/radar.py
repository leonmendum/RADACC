from dataclasses import dataclass
from typing import List
from person import Person
from publisher import Publisher
import statistics
import json


@dataclass
class Radar:
    publisher: Publisher
    frame: int = 0

    def send_message(self, people: List[Person]):
        if len(people) > 0:
            mean_speed = statistics.mean([person.speed for person in people])
        else:
            mean_speed = 0

        self.frame += 1

        data = {"speed": str(mean_speed)}

        self.publisher.publish(json.dumps(data))
