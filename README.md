# Autodistill YOLO Dataset Pipeline

A small pipeline that downloads sample images, automatically labels them (draws boxes/masks around objects in each photo), and produces a finished dataset you can use to train a YOLO object-detection model.

## Setup and usage

Step-by-step, written for anyone — no programming background assumed.

### 1. Get the code onto your computer

```
git clone https://github.com/damasonoyola/autodistill-yolo-dataset-pipeline.git
cd autodistill-yolo-dataset-pipeline
```

This downloads the folder of scripts and the sample images.

### 2. Create an isolated Python environment ("venv")

A "venv" is a private, self-contained box for installing the exact Python packages this project needs, without messing up anything else on your computer. Think of it like a separate toolbox just for this project.

```
python3 -m venv venv/autodistill
source venv/autodistill/bin/activate
```

The second command "activates" the box — your terminal prompt usually changes to show `(autodistill)` to confirm you're inside it. You'll need to run that `source` command again every time you open a new terminal and want to work on this project.

### 3. Install the required packages

Inside the activated environment:

```
pip install -r requirements.txt
```

This reads the list of every package the project depends on (specific versions included) and installs them all. It can take a while — some of these packages (PyTorch, CUDA libraries) are several gigabytes, since they include GPU support.

### 4. Set up your Hugging Face token

Some of the AI models this project uses are downloaded from Hugging Face, and downloading them requires a free account token.

1. Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) and create a "Read" token.
2. Create a file named `.env` in the project folder containing:
   ```
   HF_TOKEN=hf_your_token_here
   ```
   Type it directly into the file — never paste a token into a chat or share it anywhere.

This `.env` file is intentionally excluded from version control (via `.gitignore`), so your personal token never gets uploaded.

### 5. (Optional, side step) Download your own raw images

The dataset already includes sample images of red/green/blue soda cans, scraped ahead of time. If you wanted fresh images of something else, `scrape_soda_cans.py` is the tool for that — it searches Bing Images for a set of text queries and saves the results into `data/<color>/`:

```
python scrape_soda_cans.py --max-num 50
```

`--max-num` controls how many images to grab per category (default 50). You'd edit the `COLOR_QUERIES` dictionary at the top of the script to search for something other than soda cans. This step is independent of everything else — you only need it if you want to build a dataset from scratch.

### 6. Run the auto-labeling step

This is the core of the pipeline. `autolabel.py` loads an AI model (GroundedSAM) that can find and outline objects in photos just from a text description (here, "soda can") — no manual clicking required.

```
python autolabel.py
```

The first time you run this, it downloads a couple of large AI model files (a few GB total), so it'll be slow the first time and fast after that. When it finishes, it prints "Labeled dataset created - ready for distillation" and writes the results to `data/labeled/`:

- `images/` and `annotations/` — every labeled photo and its label data
- `train/` and `valid/` — the same data, pre-split for training (most images for training, a smaller portion held back to check accuracy)
- `data.yaml` — a small config file listing the object classes and where the images live, which a training tool reads automatically

### 7. (Optional) Visually check the labels

Auto-labeling isn't always perfect, so it helps to eyeball a sample before trusting it. `preview_labels.py` draws the boxes/masks/labels onto a handful of images and saves them as regular picture files:

```
python preview_labels.py
```

Look in `data/preview/` afterward — these are normal `.jpg` files you can open like any photo, with colored outlines and "soda can" text overlaid on each detected can. If the boxes look wrong or are missing objects, that's a sign to inspect your source images or prompt before training.

## What's next

At this point `data/labeled/` is a complete, standard YOLO-format dataset. The next stage (not yet in this repo) would be feeding `data/labeled/data.yaml` into a training tool like `ultralytics` to actually train a YOLO model — but that's a separate step from what's built here.
