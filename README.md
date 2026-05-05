# Notebook-first YOLOv8 fracture detection

This repository is a lightweight, notebook-first workflow for training a YOLOv8 object detector on a small, single-class fracture dataset.

The project intentionally keeps training inside notebooks. `main.py` is only an environment smoke test.

## Project layout

```text
notebooks/
  01_dataset_setup.ipynb          # prepare a small single-class fracture subset
  02_train_yolov8_fracture.ipynb  # train YOLOv8 on Colab or Kaggle GPU
  03_evaluate_predict.ipynb       # validate weights and save predictions
  examples/                       # original example notebooks, kept as references
main.py                           # import/version smoke test only
```

The notebooks in `notebooks/examples/` are preserved only as external references from the original repo. They are not part of the fracture workflow and may use unrelated datasets or classes.

The three fracture workflow notebooks are self-contained so they can be uploaded to Google Drive or Kaggle without needing a separate local helper module.

## Dataset format

Use an Ultralytics YOLO detection dataset with image and label split folders:

```text
fracture_subset/
  images/train/*.jpg
  images/val/*.jpg
  images/test/*.jpg
  labels/train/*.txt
  labels/val/*.txt
  labels/test/*.txt
  fracture.yaml
```

Notebook 01 can read source exports that use either `images/train` plus `labels/train` folders or Roboflow-style `train/images` plus `train/labels` folders. The prepared output is always written in the layout above.

Each label file uses one row per bounding box:

```text
0 x_center y_center width height
```

Coordinates must be normalized from `0` to `1`. The only class is:

```yaml
names:
  0: fracture
```

Do not use the full GRAZPEDWRI-DX dataset directly in this repo. Start with a small fracture-only export or subset so notebook experiments are fast and easy to inspect.

## Notebook workflow

1. Open `notebooks/01_dataset_setup.ipynb`.
   - Choose `RUN_ENV = "local"`, `"colab"`, or `"kaggle"`.
   - Point `SOURCE_DATASET` to a fracture-focused YOLO export.
   - Run the notebook to create `data/fracture_subset/fracture.yaml`.

2. Open `notebooks/02_train_yolov8_fracture.ipynb`.
   - Use a GPU runtime for real training.
   - Train from `yolov8n.pt` by default.
   - Outputs are written to `runs/fracture/train`.
   - Best weights are copied to `weights/fracture_yolov8n_best.pt`.

3. Open `notebooks/03_evaluate_predict.ipynb`.
   - Validate the trained weights.
   - Save prediction images under `runs/fracture/predict`.

## Colab notes

Set `RUN_ENV = "colab"` in each notebook. The notebooks mount Google Drive with:

```python
from google.colab import drive
drive.mount("/content/drive")
```

The project root becomes:

```text
/content/drive/MyDrive/yolov8-fracture-detection
```

Datasets, runs, and copied model weights are saved there so they persist after the Colab runtime shuts down.

## Kaggle notes

Set `RUN_ENV = "kaggle"` in each notebook.

Use Kaggle input datasets from:

```text
/kaggle/input
```

Write prepared subsets, runs, and weights to:

```text
/kaggle/working/yolov8-fracture-detection
```

For example, set `SOURCE_DATASET` in notebook 01 to a mounted Kaggle dataset path such as:

```python
SOURCE_DATASET = Path("/kaggle/input/my-fracture-yolo-dataset")
```

## Optional Roboflow source

Roboflow is optional. If you use it, export a fracture-only object detection dataset version in YOLO format, then run the Roboflow cell in `01_dataset_setup.ipynb`.

Do not hardcode or commit API keys. Set `ROBOFLOW_API_KEY` through Colab secrets, Kaggle secrets, or a local environment variable. Roboflow download code and curl URLs can include private keys, so keep those out of commits.

## Local setup

Install dependencies with your preferred Python environment. With `uv`:

```bash
uv sync
uv run python main.py
```

The smoke test imports OpenCV and Ultralytics and prints their versions. It does not train or run inference.

## What not to commit

The `.gitignore` excludes common generated artifacts. Keep these out of version control:

- Datasets and dataset exports: `data/`, `datasets/`
- Training and validation runs: `runs/`
- Model weights and exported models: `*.pt`, `*.onnx`, `*.engine`, `*.tflite`, `weights/`
- Prediction images or videos: `predictions/`, video files
- API keys, `.env` files, notebook secrets, and personal filesystem paths

## References

- Ultralytics YOLO detection dataset format: https://docs.ultralytics.com/datasets/detect/
- Ultralytics training mode: https://docs.ultralytics.com/modes/train/
- Ultralytics validation mode: https://docs.ultralytics.com/modes/val/
- Ultralytics prediction mode: https://docs.ultralytics.com/modes/predict/
- Roboflow dataset export docs: https://docs.roboflow.com/datasets/dataset-versions/exporting-data
- Roboflow export API docs: https://docs.roboflow.com/developer/rest-api/export-data
- Colab Drive file I/O notebook: https://colab.research.google.com/notebooks/io.ipynb
- Kaggle notebooks docs: https://www.kaggle.com/docs/notebooks
