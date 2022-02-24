# video settings
useCam = False
input = "" if useCam else "../videos/flurVideo2.mp4"
output = "../videos/flurTestEvenMoreStuffelsWithBoxesForwardLonger.mp4"
confidence = 0.5
skipFrames = 1
skipVideoFrames = 0
countingLineHeightFactor = 0.65 if 'airport' in input else 0.66
frameWidth = 800
net = 'faster'
showBoxes = False
printBoxDimensions = False
showProcessingTime = True


# model settings
if net == 'mask':
    file = "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"
    weights = "detectron2://COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x/137849600/model_final_f10217.pkl"
elif net == 'faster':
    file = "COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml"
    weights = "detectron2://COCO-Detection/faster_rcnn_R_101_FPN_3x/137851257/model_final_f6e8b1.pkl"

useCpu = False


## MASK RCNN
# file = "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"
# weights = "detectron2://COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x/137849600/model_final_f10217.pkl"

## FASTER RCNN
# file = "COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml"
# weights = "detectron2://COCO-Detection/faster_rcnn_R_101_FPN_3x/137851257/model_final_f6e8b1.pkl"


