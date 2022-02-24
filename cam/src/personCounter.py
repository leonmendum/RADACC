import sys
import cv2.cv2 as cv
import detectron2
from torchvision.utils import draw_bounding_boxes

from cam.helpers import constants, pyTorch as pT, settings, mqttPublisher, functions
from cam.helpers.centroidTracker import CentroidTracker
from cam.helpers.trackableObject import TrackableObject
from imutils.video import FPS
import numpy as np
import imutils
import dlib
from datetime import datetime
import torch


# prototxt = 'neuralNet/MobileNetSSD_deploy.prototxt'
# model = 'neuralNet/MobileNetSSD_deploy.caffemodel'
#
# CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
#            "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
#            "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
#            "sofa", "train", "tvmonitor"]
#

# load our serialized model from disk
# net = cv.dnn.readNetFromCaffe(prototxt, model)

class personCounter:
    def __init__(self, uuid, roomId):
        self.uuid = uuid
        self.roomId = roomId

    def run(self):
        # Create predictor
        print("[INFO] loading model...")
        cfg, predictor = pT.getPredictorFromPytorch()

        classes1 = pT.getClassesFromMetadata(cfg)
        # if a video path was not supplied, grab a reference to the webcam
        if settings.useCam:
            print("[INFO] starting video stream...")
            vs = cv.VideoCapture(0)
            if not vs.isOpened():
                vs = cv.VideoCapture(1)
                print("[ERROR] could not open camera 1! Trying cam 0.")
            if not vs.isOpened():
                print("[ERROR] could not open camera! Exiting program.")
                sys.exit()

        # otherwise, grab a reference to the video file
        else:
            print("[INFO] opening video file...")
            vs = cv.VideoCapture(settings.input)
            if not vs.isOpened():
                print("[ERROR] could not open video! Exiting program.")
                sys.exit()

        # initialize the video writer (we'll instantiate later if need be)
        writer = None
        # initialize the frame dimensions (we'll set them as soon as we read
        # the first frame from the video)
        W = None
        H = None
        # instantiate our centroid tracker, then initialize a list to store
        # each of our dlib correlation trackers, followed by a dictionary to
        # map each unique object ID to a TrackableObject
        print("[INFO] initialize centroid tracker...")
        ct = CentroidTracker(maxDisappeared=3, maxDistance=50)
        trackers = []
        trackableObjects = {}
        # initialize the total number of frames processed thus far, along
        # with the total number of objects that have moved either up or down
        totalFrames = 0
        totalEnter = 0
        totalExit = 0
        totalInRoom = 0
        # start the frames per second throughput estimator
        fps = FPS().start()
        outputs = []

        if settings.skipVideoFrames > 0:
            print("[INFO] skipping frames...")
            for i in range(0, settings.skipVideoFrames):
                frame = vs.read()

        # initialize publisher
        print("[INFO] initializing publisher...")
        pub = mqttPublisher.Publisher()
        initMessage = {
            "header": "Ei Gude",
            "payload": ", wie?",
            "name": "personCounter1"
        }
        pub.publish(functions.createJsonFromDict(initMessage), self.roomId)
        maskImage = []
        print("[INFO] Starting main loop. Press Q to abort.")

        # loop over frames from the video stream
        while True:
            # grab the next frame and handle if we are reading from either
            # VideoCapture or VideoStream
            frame = vs.read()

            # current date and time
            datePic = datetime.utcnow()
            timestampPic = datetime.timestamp(datePic)

            if 'example' in settings.input and (totalFrames == 50):
                print("\n\n[INFO] skipping even more frames...\n\n")
                for i in range(0, 140):
                    frame = vs.read()
                    totalFrames += 1

            print(f"\nFrame {totalFrames}")

            frame = frame[1]
            # if we are viewing a video and we did not grab a frame then we
            # have reached the end of the video
            if settings.input is not None and frame is None:
                break
            # resize the frame to have a maximum width of 500 pixels (the
            # less data we have, the faster we can process it), then convert
            # the frame from BGR to RGB for dlib
            frame = imutils.resize(frame, width=settings.frameWidth)
            original = frame.copy()
            rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            # if the frame dimensions are empty, set them
            if W is None or H is None:
                (H, W) = frame.shape[:2]
            # if we are supposed to be writing a video to disk, initialize
            # the writer
            if settings.output is not None and writer is None:
                fourcc = cv.VideoWriter_fourcc(*"mp4v")
                writer = cv.VideoWriter(settings.output, fourcc, 30, (W, H), True)

                # initialize the current status along with our list of bounding
                # box rectangles returned by either (1) our object detector or
                # (2) the correlation trackers
            status = "Waiting"
            rects = []
            # check to see if we should run a more computationally expensive
            # object detection method to aid our tracker
            if totalFrames % settings.skipFrames == 0:
                # set the status and initialize our new set of object trackers
                status = "Detecting"
                trackers = []
                # convert the frame to a blob and pass the blob through the
                # network and obtain the detections
                # blob = cv.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)
                # net.setInput(blob)
                # detections = net.forward()
                outputs = pT.predict(frame, predictor)

                # loop over the detections
                instances = outputs['instances'].to('cpu')
                scores = instances.scores.numpy()
                pBoxes = instances.pred_boxes.tensor.numpy()
                pClasses = instances.pred_classes.numpy()
                cls = np.asarray([], np.int)
                box = np.empty((0, 4), np.int)
                scores2 = np.asarray([], np.int)


                for i in range(0, len(instances)):
                    if classes1[pClasses[i]] == "person":
                        cls = np.append(cls, pClasses[i])
                        box = np.append(box, np.array([pBoxes[i]]), axis=0)
                        scores2 = np.append(scores2, scores[i])

                obj = detectron2.structures.Instances(image_size=(450, 800))
                obj.set('pred_classes', cls)
                obj.set('pred_boxes', box)
                obj.set('scores', scores2)

                if outputs:
                    maskImage = pT.getVisualizerImage(original, obj, cfg)
                    maskImage = cv.UMat(maskImage)
                    # cv.imshow("maskImage", maskImage)
                    cv.setWindowTitle("maskImage", f"maskImage frame {totalFrames}")

                # pMasks = instances.pred_masks.numpy()
                for i in np.arange(0, len(instances)):
                    # extract the confidence (i.e., probability) associated
                    # with the prediction
                    #  confidence = detections[0, 0, i, 2]
                    confidence = scores[i]
                    # filter out weak detections by requiring a minimum
                    # confidence
                    if confidence > settings.confidence:
                        # extract the index of the class label from the
                        # detections list
                        # idx = int(detections[0, 0, i, 1])
                        idx = pClasses[i]
                        # if the class label is not a person, ignore it
                        if classes1[idx] != "person":
                            continue

                        # compute the (x, y)-coordinates of the bounding box
                        # for the object

                        # box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                        box = pBoxes[i]
                        (startX, startY, endX, endY) = box.astype("int")
                        if settings.showBoxes:
                            cv.rectangle(frame, (startX, startY), (endX, endY), (250, 230, 130), 2)
                            cv.putText(frame, "detection", (startX - 20, startY - 20),
                                       cv.FONT_HERSHEY_SIMPLEX, 0.5, (250, 230, 130), 2)
                        # construct a dlib rectangle object from the bounding
                        # box coordinates and then start the dlib correlation
                        # tracker
                        tracker = dlib.correlation_tracker()
                        rect = dlib.rectangle(startX, startY, endX, endY)
                        tracker.start_track(rgb, rect)
                        # add the tracker to our list of trackers so we can
                        # utilize it during skip frames
                        trackers.append(tracker)

                # otherwise, we should utilize our object *trackers* rather than
                # object *detectors* to obtain a higher frame processing throughput
                # loop over the trackers

                pBoxCount = 0

                if settings.printBoxDimensions:
                    print(f"frame: {totalFrames}")
                    for i in np.arange(0, len(pBoxes)):
                        if classes1[pClasses[i]] == 'person':
                            print(f"pbox {pBoxCount}")
                            (pBoxX, pBoxY, pBoxEndX, pBoxEndY) = pBoxes[i].astype("int")
                            print(f"{[(pBoxX, pBoxY), (pBoxEndX, pBoxEndY)]}")
                            pBoxCount += 1

                    print("--------------")

                boxCount = 0
                for tracker in trackers:
                    # set the status of our system to be 'tracking' rather
                    # than 'waiting' or 'detecting'
                    status = "Tracking"
                    # update the tracker and grab the updated position
                    tracker.update(rgb)
                    pos = tracker.get_position()
                    # unpack the position object
                    startX = abs(int(pos.left()))
                    startY = abs(int(pos.top()))
                    endX = abs(int(pos.right()))
                    endY = abs(int(pos.bottom()))
                    rects.append((startX, startY, endX, endY))
                    if settings.printBoxDimensions:
                        print(f"box {boxCount}")
                        print(f"{[(startX, startY), (endX, endY)]}")

                    boxCount += 1

                if settings.printBoxDimensions:
                    print(f"\n")
            # add the bounding box coordinates to the rect
            # draw a horizontal line in the center of the frame -- once an
            # object crosses this line we will determine whether they were
            # moving 'up' or 'down'

            cv.line(frame, (0, int(settings.countingLineHeightFactor * H)), (W, int(settings.countingLineHeightFactor * H)),
                    (0, 255, 255), 2)
            # cv.line(maskImage, (0, int(settings.countingLineHeightFactor * H)), (W, int(settings.countingLineHeightFactor * H)),
            #         (0, 255, 255), 2)

            if settings.showBoxes:
                for rect in rects:
                    cv.rectangle(frame, (rect[0], rect[1]), (rect[2], rect[2]),
                                 (140, 30, 30), 2)
                    cv.putText(frame, "tracking", (rect[0] - 20, rect[1] - 5),
                               cv.FONT_HERSHEY_SIMPLEX, 0.5, (140, 30, 30), 2)

            # use the centroid tracker to associate the (1) old object
            # centroids with (2) the newly computed object centroids
            objects = ct.update(rects)

            # loop over the tracked objects
            for (objectID, centroid) in objects.items():
                # check to see if a trackable object exists for the current
                # object ID
                to = trackableObjects.get(objectID, None)
                # if there is no existing trackable object, create one
                if to is None:
                    to = TrackableObject(objectID, centroid)

                # otherwise, there is a trackable object so we can utilize it
                # to determine direction
                else:
                    # the difference between the y-coordinate of the *current*
                    # centroid and the mean of *previous* centroids will tell
                    # us in which direction the object is moving (negative for
                    # 'up' and positive for 'down')
                    prevCentrYCoords = [c[1] for c in to.centroids]
                    direction = centroid[1] - np.mean(prevCentrYCoords)
                    # print(f"direction of {to.objectID}: {direction}")
                    to.centroids.append(centroid)
                    cutoffLine = int(settings.countingLineHeightFactor * H)
                    # check to see if the object has been counted or not
                    # if the direction is negative (indicating the object
                    # is moving up) AND the centroid is above the center
                    # line, count the object
                    if direction < 0:
                        # check if current is below AND previous centroid above counting line print(f"ID: {to.objectID},
                        # previous: {prevCentrYCoords[len(prevCentrYCoords) - 1]}, cutoff: {cutoffLine},
                        # current: {centroid[1]}")
                        if len(prevCentrYCoords) > 0 and prevCentrYCoords[len(prevCentrYCoords) - 1] >= cutoffLine >= \
                                centroid[1]:
                            totalExit += 1
                            totalInRoom -= 1 if totalInRoom > 0 else 0
                            to.currentDirection = constants.UP

                    # if the direction is positive (indicating the object
                    # is moving down) AND the centroid is below the
                    # center line, count the object
                    elif direction > 0:
                        if len(prevCentrYCoords) > 0 and prevCentrYCoords[len(prevCentrYCoords) - 1] <= cutoffLine <= \
                                centroid[1]:
                            totalEnter += 1
                            totalInRoom += 1
                            to.currentDirection = constants.DOWN

                # store the trackable object in our dictionary
                trackableObjects[objectID] = to
                # draw both the ID of the object and the centroid of the
                # object on the output frame
                text = "ID {} ".format(objectID)

                cv.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
                           cv.FONT_HERSHEY_SIMPLEX, 0.5, constants.colourMovementMap[to.currentDirection], 2)
                cv.circle(frame, (centroid[0], centroid[1]), 2, constants.colourMovementMap[to.currentDirection], -1)

                # cv.putText(maskImage, text, (centroid[0] - 10, centroid[1] - 10),
                #            cv.FONT_HERSHEY_SIMPLEX, 0.5, constants.colourMovementMap[to.currentDirection], 2)
                # cv.circle(maskImage, (centroid[0], centroid[1]), 2, constants.colourMovementMap[to.currentDirection], -1)

            # construct a tuple of information we will be displaying on the
            # frame
            info = [
                ("Exit", totalExit),
                ("Enter", totalEnter),
                ("Status", status),
            ]
            # loop over the info tuples and draw them on our frame
            for (i, (k, v)) in enumerate(info):
                text = "{}: {}".format(k, v)
                cv.putText(frame, text, (10, H - ((i * 20) + 20)),
                           cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                # cv.putText(maskImage, text, (10, H - ((i * 20) + 20)),
                #            cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            cv.putText(frame, f"Currently in room: {totalInRoom}", (int(0.6 * W), int(0.9 * H)),
                       cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            # cv.putText(maskImage, f"Currently in room: {totalInRoom}", (int(0.6 * W), int(0.9 * H)),
            #            cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            # check to see if we should write the frame to disk
            if writer is not None:
                #writer.write(frame)
                writer.write(maskImage)
            # show the output frame
            cv.imshow("Frame", frame)
            cv.imshow("maskImage", maskImage)
            camText = "Camera"
            cv.setWindowTitle("Frame", f"Frame {totalFrames}. Filename: {settings.input if settings.input else camText}")

            print(f"Total points tracked: {len(objects)}. Exited: {totalExit}. Entered: {totalEnter}")
            dateSend = datetime.utcnow()
            timestampSend = datetime.timestamp(dateSend)
            pub.createAndSendMessage(self.roomId, datePic, totalFrames, len(objects), totalEnter,
                                     totalExit, totalInRoom)
            key = cv.waitKey(1) & 0xFF
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break
            # increment the total number of frames processed thus far and
            # then update the FPS counter
            totalFrames += 1
            fps.update()

        # stop the timer and display FPS information
        fps.stop()
        print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
        # check to see if we need to release the video writer pointer

        print("[INFO] dismantling MQTT publisher")
        pub.dismantle()

        if writer is not None:
            writer.release()
        # if we are not using a video file, stop the camera video stream
        # otherwise, release the video file pointer
        vs.release()
        # close any open windows
        cv.destroyAllWindows()
