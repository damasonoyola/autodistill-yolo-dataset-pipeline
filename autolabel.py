# source ~/venv/autodistill/bin/activate

import glob
import os
import shutil

from dotenv import load_dotenv
load_dotenv()
from autodistill_grounded_sam import GroundedSAM
from autodistill.detection import CaptionOntology

base_model = GroundedSAM(
    ontology=CaptionOntology({
        "soda can": "soda can",
    })
)

# label() doesn't recurse into subfolders, so flatten the color folders
# into one combined folder before labeling
combined_dir = "./data/all"
os.makedirs(combined_dir, exist_ok=True)

for color in ("red", "green", "blue"):
    for src in glob.glob(f"./data/{color}/*.jpg"):
        dst = os.path.join(combined_dir, f"{color}_{os.path.basename(src)}")
        if not os.path.exists(dst):
            shutil.copy(src, dst)

base_model.label(combined_dir, extension=".jpg", output_folder="./data/labeled")
