import paho.mqtt.client as mqtt


class Publisher:
    topic: str
    client = mqtt.Client("Python")
    conencted = False

    def __init__(self, broker: str, port: int, topic: str) -> None:
        self.topic = topic
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

    def publish(self, message: str):
        self.client.publish(self.topic, message)

    def dismantle(self):
        self.client.disconnect()
        self.client.loop_stop()
