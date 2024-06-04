from ultralytics import YOLO

# Load a model
#model = YOLO('yolov8n.pt')  # load an official model
#model = YOLO('/Users/alainfrey/Library/CloudStorage/GoogleDrive-alain.frey@outlook.com/My Drive/detect/detect1280b16ep200/weights/best.pt')  # load a custom model
#model = YOLO('/Users/alainfrey/Library/CloudStorage/GoogleDrive-alain.frey@outlook.com/My Drive/detect1280b16ep200custom138/train/weights/best.pt')  # load a custom model
model = YOLO('/Users/alainfrey/Library/CloudStorage/GoogleDrive-alain.frey@outlook.com/My Drive/seg1920-200-customcombined-aug-fullsize/train/weights/best.pt')
#alidation_results = model.val(data='/Users/alainfrey/Downloads/BeachesIceland-allvalsplit/data.yaml', imgsz=1280,  split='val')
#alidation_results = model.val(data='/Users/alainfrey/Downloads/BeachesIceland-6/data.yaml', device='mps', imgsz=1920, split='test')

#model.export(format='onnx')
#alidation_results = model.val(data='/Users/alainfrey/Downloads/BeachesIceland-9/data.yaml', imgsz=1280, split='test')
#source='/Users/alainfrey/Downloads/DJI_0159.MP4'
#model.predict(source, device='mps', show=True, imgsz=1920)
#/Users/alainfrey/Downloads/BeachesIceland-allvalsplit/data.yaml

results = model.predict("/Users/alainfrey/Library/CloudStorage/GoogleDrive-alain.frey@outlook.com/My Drive/detect1280b16ep200custom138/train/train_batch1.jpg", imgsz=1280, conf=0.5, device='mps')