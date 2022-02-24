import json
import cv2.cv2 as cv


def createJsonFromDict(d):
    return json.dumps(d, indent=4)


def getCameras():
    is_working = True
    dev_port = 0
    working_ports = []
    available_ports = []
    while is_working:
        camera = cv.VideoCapture(dev_port)
        if not camera.isOpened():
            is_working = False
        else:
            is_reading, img = camera.read()
            if is_reading:
                working_ports.append(dev_port)
            else:
                available_ports.append(dev_port)
        dev_port += 1
    return available_ports, working_ports
