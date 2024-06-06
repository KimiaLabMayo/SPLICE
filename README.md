# SPLICE: Patch Collage Generator

[[`Arxiv`]](https://arxiv.org/abs/2404.17704)

Areej Alsaafin, Peyman Nejat, Abubakr Shafique, Jibran Khan, Saghir Alfasly, Ghazal Alabtah, H.R.Tizhoosh

## Overview
SPLICE is a patch selection method designed to create a collage from a collection of whole slide image patches. This repository contains the Python implemantation of SPLICE. It utilizes color histograms to selectively remove similar patches, creating a visually cohesive collage. 

## Features
- **Patch Selection:** Utilizes color histogram comparison to select the most selective patches of the whole slide image.
- **Dynamic Thresholding:** Allows for customizable inclusion criteria with a percentile threshold.
- **Efficient Processing:** Resizes patches for faster color histogram computation without compromising on the quality of the final collage.

## Requirements
To run SPLICE, you will need:
- Python 3.x
- OpenCV (`cv2`)
- NumPy
- Pillow (PIL)

## Installation
Ensure you have Python installed on your system. You can then install the required libraries using pip:

```bash
pip install numpy opencv-python pillow
```


## Usage
To use SPLICE in your project, first import the function and then call it with your patches and their coordinates:

```python
from splice import splice

# Assuming patches_np is your array of patch images as numpy arrays
# and patches_xy is an array of their corresponding (x, y) coordinates
collage = splice(patches_np, patches_xy, thresh=30)
```

`patches_np` should be a NumPy array of your patches, and `patches_xy` should be a NumPy array of the (x, y) coordinates for each patch. `thresh` is an optional parameter that determines the percentile for including or excluding patches based on their color histogram similarity. The default value is 30. the function returns a collage of selected patches as a NumPy array.

