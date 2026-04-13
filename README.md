# Historical Meta-Data Extraction

Code for the publication **"From Film to Data: Automating Meta-Feature Extraction in Historical Aerial Imagery"**.

This repository provides tools to automatically extract camera metadata (camera ID, focal length, flight height, fiducial marks) from scanned historical aerial images.

---

## Repository Structure

```
data/
  dlib/                   # Pre-trained DLIB detector models for fiducial-mark subset detection
    detector_subset_E.svm
    detector_subset_N.svm
    detector_subset_S.svm
    detector_subset_W.svm

src/
  display/
    display_images.py         # Matplotlib-based image display with annotation support
  estimate/
    estimate_cam_id.py        # Estimate camera ID from images with similar properties
    estimate_fid_mark.py      # Estimate fiducial mark coordinates by averaging neighbours
    estimate_focal_length.py  # Estimate focal length from images in the same flight strip
    estimate_height.py        # Estimate flight height from images in the same flight strip
    estimate_subset.py        # Estimate subset bounding boxes for fiducial mark regions
  fid_marks/
    calculate_fid_mark.py     # Compute corner fid marks (NE/NW/SE/SW) from line intersections
    extract_fid_mark.py       # Detect N/E/S/W fiducial marks via Hough lines and circle fitting
    extract_subset.py         # Locate fid-mark subsets using a pre-trained DLIB detector
  text/
    altimeter_snippets.py     # Geometry helpers for altimeter pointer detection
    extract_altimeter.py      # Full altimeter reading pipeline (detect → locate circle → read pointer)
    extract_text.py           # OCR-based text extraction using PaddleOCR
    find_cam_id.py            # Parse extracted text to find a camera ID
    find_focal_length.py      # Parse extracted text to find a focal length value
    find_height.py            # Parse extracted text to find a flight height value
```

---

## Requirements

- Python 3.10+
- [OpenCV](https://opencv.org/) (`cv2`)
- [dlib](http://dlib.net/)
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- [NumPy](https://numpy.org/), [SciPy](https://scipy.org/), [pandas](https://pandas.pydata.org/), [Shapely](https://shapely.readthedocs.io/)
- [Matplotlib](https://matplotlib.org/)

---

## Usage

### Extract fiducial marks from an image

```python
from src.fid_marks.extract_subset import extract_subset
from src.fid_marks.extract_fid_mark import extract_fid_mark

# Locate the subset region for the north fiducial mark
bounds = extract_subset(image, key="n")

# Extract the precise fid mark coordinates within that subset
fid_coords = extract_fid_mark(image, key="n", subset_bounds=bounds)
print(fid_coords)  # (x, y) in image coordinates
```

### Read the altimeter from an image

```python
from src.text.extract_altimeter import extract_altimeter

height = extract_altimeter(image)
print(f"Altimeter reading: {height} ft")
```

### Extract text and parse metadata

```python
from src.text.extract_text import extract_text
from src.text.find_focal_length import find_focal_length
from src.text.find_height import find_height

texts, positions, confidences = extract_text(image)
combined = ";".join(texts)

focal_length = find_focal_length(combined)
height = find_height(combined)
```

### Estimate values from neighbouring images

```python
import pandas as pd
from src.estimate.estimate_focal_length import estimate_focal_length

# Provide a DataFrame with columns: image_id, focal_length, focal_length_estimated
focal_length_data = pd.read_csv("focal_length_data.csv")
focal_length = estimate_focal_length("CA173632V0009", focal_length_data=focal_length_data)
```

---

## Citation

If you use this code, please cite the associated publication:

> *From Film to Data: Automating Meta-Feature Extraction in Historical Aerial Imagery*
