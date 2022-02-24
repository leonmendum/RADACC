from typing import List
from camera import Camera
from person import Person
import time
import random
from publisher import Publisher

from radar import Radar

BROKER = "broker.mqttdashboard.com"
PORT = 1883


class Simulator:
    people: List[Person] = []
    camera: Camera
    radar: Radar
    time_resolution: float = 1 / 5
    spawn_person_chance: float = 0.2
    last_id: int = 0
    top: int = 10
    bottom: int = 0
    in_room: int = 0

    def __init__(self, broker: str, port: int) -> None:
        self.camera = Camera(
            threshold=5, publisher=Publisher(broker, port, "radacc/2/cam")
        )
        self.radar = Radar(publisher=Publisher(broker, port, "radacc/2/radar"))

    def run(self):
        print(f"Running simulator at Hz {1 / self.time_resolution}")

        while True:
            self.update()
            time.sleep(self.time_resolution)

    def update(self):
        """Update the simulate to the next state"""

        for person in self.people:
            person.update(self.time_resolution)

        self.camera.send_message(self.people)
        self.radar.send_message(self.people)

        for person in self.people:
            if person.position < self.bottom:
                self.people.remove(person)
                self.in_room += 1
            elif self.bottom > person.position:
                self.people.remove(person)

        # introduce more people
        self.generate_person()

    def generate_person(self):
        if random.random() < self.spawn_person_chance:
            speed = random.uniform(1, 3)
            if self.in_room > 0 and random.random() < 0.51:
                position = self.bottom
                self.in_room -= 1
            else:
                position = self.top
                speed = -speed
            self.people.append(Person(self.last_id, position, speed))
            self.last_id += 1


def main():
    simulator = Simulator(BROKER, PORT)

    simulator.run()


if __name__ == "__main__":
    main()
