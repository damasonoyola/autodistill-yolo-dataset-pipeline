import os
from pathlib import Path

import cv2
import supervision as sv

IMAGES_DIRECTORY_PATH = "./data/labeled/train/images"
ANNOTATIONS_DIRECTORY_PATH = "./data/labeled/train/labels"
DATA_YAML_PATH = "./data/labeled/data.yaml"
OUTPUT_DIRECTORY_PATH = "./data/preview"

SAMPLE_SIZE = 16

dataset = sv.DetectionDataset.from_yolo(
    images_directory_path=IMAGES_DIRECTORY_PATH,
    annotations_directory_path=ANNOTATIONS_DIRECTORY_PATH,
    data_yaml_path=DATA_YAML_PATH,
)

print(len(dataset))

mask_annotator = sv.MaskAnnotator()
box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()

os.makedirs(OUTPUT_DIRECTORY_PATH, exist_ok=True)

for i, (image_path, image, annotation) in enumerate(dataset):
    if i == SAMPLE_SIZE:
        break
    annotated_image = image.copy()
    annotated_image = mask_annotator.annotate(
        scene=annotated_image, detections=annotation)
    annotated_image = box_annotator.annotate(
        scene=annotated_image, detections=annotation)
    labels = [dataset.classes[class_id] for class_id in annotation.class_id]
    annotated_image = label_annotator.annotate(
        scene=annotated_image, detections=annotation, labels=labels)

    output_path = os.path.join(OUTPUT_DIRECTORY_PATH, Path(image_path).name)
    cv2.imwrite(output_path, annotated_image)
