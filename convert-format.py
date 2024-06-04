from ultralytics import YOLO

# Load a model
#model = YOLO('yolov8n.pt')  # load an official model
#model = YOLO('/Users/alainfrey/Library/CloudStorage/GoogleDrive-alain.frey@outlook.com/My Drive/detect/detect1280b16ep200/weights/best.pt')  # load a custom model
#model = YOLO('/Users/alainfrey/Library/CloudStorage/GoogleDrive-alain.frey@outlook.com/My Drive/detect1280b16ep200custom138/train/weights/best.pt')  # load a custom model
model = YOLO('/Users/alainfrey/Library/CloudStorage/GoogleDrive-alain.frey@outlook.com/My Drive/seg1920-200-customcombined-aug-fullsize/train/weights/best.pt')

model.export(format="onnx")