# MOVEMENT
NONE = 0
UP = 1
DOWN = 2

# COLOURS
green = (0, 255, 0)
blue = (255, 0, 0)
red = (0, 0, 255)

colourMovementMap = dict([
    (NONE, green),
    (UP, blue),
    (DOWN, red)
])


# MQTT
brokerAddress = "broker.mqttdashboard.com"
port = 1883
topic = "radacc/{room}/cam"
