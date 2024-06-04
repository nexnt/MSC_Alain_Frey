import torch

# Load the model
model_path = 'segmentation/SegmentationInitial200/best.pt'
model = torch.load(model_path)

# Print the model structure
print(model)