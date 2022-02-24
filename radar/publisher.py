import paho.mqtt.client as mqtt
import json


class Publisher:
    def __init__(self, name: str, broker: str, port: int):
        self.name = name
        self.connected = False
        self.client = mqtt.Client("Python")

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

        self.client.connect(broker, port=port)  # connect to broker
        self.client.loop_start()  # start the loop

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker")
            self.connected = True  # Signal connection
        else:
            print("Connection failed")

    def on_disconnect(self, client, userdata, rc):
        print("Disconnected from broker")
        self.connected = False

    def publish(self, msg):
        # print(f"msg: {msg}")
        self.client.publish("radar", msg)

    def dismantle(self):
        self.client.disconnect()
        self.client.loop_stop()

    def createAndSendMessage(
        self, speed: float, temperature: float, firmware: dict, device: dict
    ):
        data = {
            "name": self.name,
            "speed": speed,
            "temperature": temperature,
            "firmware": str(firmware),
            "devive": str(device),
        }

        self.publish(json.dumps(data))
