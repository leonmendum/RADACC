# import some common detectron2 utilities
import time

import numpy as np
import torch
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.model_zoo import model_zoo
from detectron2.utils.visualizer import Visualizer, ColorMode
from detectron2.data import MetadataCatalog
import cv2.cv2 as cv
from torchvision.utils import draw_bounding_boxes

from cam.helpers import settings


def getPredictorFromPytorch():
    torch.device('cuda')
    if settings.useCpu:
        torch.device('cpu')

    # Create config
    conf = get_cfg()

    # model_file = "COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml"
    # cfg.MODEL.WEIGHTS = "detectron2://COCO-Detection/faster_rcnn_R_101_FPN_3x/137851257/model_final_f6e8b1.pkl"
    model_file = settings.file
    conf.merge_from_file(model_zoo.get_config_file(model_file))
    conf.MODEL.ROI_HEADS.SCORE_THRESH_TEST = settings.confidence  # set threshold for this model
    conf.MODEL.WEIGHTS = settings.weights
    if settings.useCpu:
        conf.MODEL.DEVICE = 'cpu'

    # Create predictor
    p = DefaultPredictor(conf)
    return conf, p


def  predict(f, pred):
    # Make prediction
    start = time.time()
    outs = pred(f)
    end = time.time()
    elapsed = format(end - start, ".2f")
    if settings.showProcessingTime:
        print(f"processing time p. frame: {elapsed}s")
    return outs


# cap = cv.VideoCapture("videos/crossing.mp4")


def getMetadata(conf):
    return MetadataCatalog.get(conf.DATASETS.TRAIN[0])

def getClassesFromMetadata(conf):
    meta = getMetadata(conf)
    return meta.thing_classes

def getVisualizerImage(f, out, conf):
    v = Visualizer(f[:, :, ::-1],
                   getMetadata(conf),
                   #instance_mode=ColorMode.SEGMENTATION,
                   scale=1)
    v = v.draw_instance_predictions(out)
    img = v.get_image()[:, :, ::-1]
    return img


def getBoundingBoxInfo(out):
    boxes = out['instances'].to("cpu").pred_boxes.tensor.numpy()
    return boxes


def getBlankImageWithBoxes(boxes, f):
    img = np.zeros(f.shape, dtype="uint8")
    for box in boxes:
        print(f"box: {box}")
        x = (int(box[0]), int(box[1]))
        y = (int(box[2]), int(box[3]))
        print(f"(x,y)): {(x, y)}")
        cv.rectangle(img, x, y, (75, 150, 225), 1)

    return img


# # Create predictor
# cfg, predictor = getPredictorFromPytorch()
#
# classes = getClassesFromMetadata(cfg)
#
# cap = cv.VideoCapture(1)
# if not cap.isOpened():
#     cap = cv.VideoCapture(0)
#
# while True:
#     # grab the next frame and handle if we are reading from either
#     # VideoCapture or VideoStream
#     _, frame = cap.read()
#
#     outputs = predict(frame, predictor)
#
#     image = getVisualizerImage(frame, outputs, cfg)
#     cv.imshow("", image)
#
#     # get bounding box info
#     predBoxes = getBoundingBoxInfo(outputs)
#
#     blankImg = getBlankImageWithBoxes(predBoxes, frame)
#     cv.imshow("boxes", blankImg)
#
#     key = cv.waitKey(1) & 0xFF
#     # if the `q` key was pressed, break from the loop
#     if key == ord("q"):
#         break
