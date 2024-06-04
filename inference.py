from ultralytics import YOLO

model = YOLO('best.pt')

results = model.val(data='/Users/alainfrey/Documents/yolo/datasets/roboflow2/data.yaml',device='mps')