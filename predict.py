import random
import numpy as np
from ultralytics import YOLO
from PIL import Image
import cv2

# Load a pretrained YOLOv8n-seg Segment model
#model = YOLO('runs/detect/train23/weights/best.pt')
#model = YOLO('yolov8x-seg.pt')
#model = YOLO("segmentation/SegmentationInitial200/best.pt")
model = YOLO("/Users/alainfrey/Library/CloudStorage/GoogleDrive-alain.frey@outlook.com/My Drive/detect1280b16ep200custom138/train/weights/best.pt")  # Adjust the model path and name as necessary

# Run inference on an image
results = model.track('/Users/alainfrey/Lichtwinkel Dropbox/Alain Frey/thesis/strandkirkja/good/DJI_0210.MP4', imgsz=1280, show=True, device='mps')  # results list
#model.val()


cv2.waitKey(0)
