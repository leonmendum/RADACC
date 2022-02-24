import paho.mqtt.client as mqttClient

from cam.helpers import constants
from cam.helpers.functions import createJsonFromDict


class Publisher:
    def __init__(self):
        self.connected = False
        self.client = mqttClient.Client("Python")

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

        self.client.connect(constants.brokerAddress, port=constants.port)  # connect to broker
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

    def publish(self, msg, roomId):
        # print(f"msg: {msg}")
        topic = constants.topic.replace("{room}", str(roomId))
        self.client.publish(topic, msg)

    def dismantle(self):
        self.client.disconnect()
        self.client.loop_stop()

    def createAndSendMessage(self, roomId, datePic, totalFrames, totalDetected, totalEnter, totalExit, totalInRoom):
        msgDict = {
            "datetimePicture": str(datePic.isoformat()),
            "totalFrames": totalFrames,
            "totalDetected": totalDetected,
            "totalEnter": totalEnter,
            "totalExit": totalExit,
            "totalInRoom": totalInRoom
        }
        # Serializing json
        json_object = createJsonFromDict(msgDict)
        print(json_object)
        self.publish(json_object, roomId)


