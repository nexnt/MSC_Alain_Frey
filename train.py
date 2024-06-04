from ultralytics import YOLO

# Load a model
#model = YOLO('yolov8n.yaml')  # build a new model from YAML
model = YOLO('yolov8n.pt')  # load a pretrained model (recommended for training)
#model = YOLO('yolov8n.yaml').load('yolov8n.pt')  # build from YAML and transfer weights
#model = YOLO('runs/detect/train23/weights/last.pt')
#model = YOLO('yolov8n-seg.pt')  # load a pretrained model (recommended for training)


# Train the model with 2 GPUs
results = model.train(data='/Users/alainfrey/Documents/yolo/datasets/export4/data.yaml', epochs=2000, plots=True,device='mps')


#metrics = model.val()  # evaluate model performance on the validation set
#results = model(test_image)  # predict on an image
path = model.export(format="onnx")  # export the model to ONNX format
