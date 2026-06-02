# Image Padding & Resize Utility

## Overview

Image Padding & Resize Utility is a lightweight dataset preparation tool designed to standardize image dimensions for AI training workflows.

The utility automatically resizes images while preserving their original aspect ratio, then centers them within a 1024×1024 canvas. Any unused space is padded using a pure black background.

This approach helps create dimensionally consistent datasets without introducing image distortion that can occur when stretching or forcing images into a fixed resolution.


## Features

- Standardizes images to 1024×1024 resolution

- Preserves original aspect ratio

- Automatically centers images on the canvas

- Uses pure black padding for unused space

- Supports:

  - JPG

  - JPEG

  - PNG

  - WEBP

- Processes folders and subfolders automatically

- Simple drag-and-drop workflow


## Usage

1. Place images inside a folder.

2. Drag and drop the folder onto:

```
`image\_padding\_dragdrop.bat`
```

3. The utility will:

   - Scan the folder and all subfolders

   - Resize images proportionally

   - Create a centered 1024×1024 canvas

   - Pad remaining space with black pixels

   - Save the processed image over the original file


## Example

Original Image:

```
`600 × 900`
```

Processed Image:

```
`1024 × 1024`
```

The image remains proportional and centered while unused canvas space is filled with black padding.


## Why This Tool Exists

Many AI training datasets contain images with inconsistent resolutions and aspect ratios.

Manually resizing and padding hundreds or thousands of images can require significant time and repetitive effort.

This utility was developed to automate dataset normalization and provide a fast, repeatable method for preparing images for training workflows.

## Important Note: This Tool Does Not Upscale Images

This utility does not enlarge or upscale low-resolution images.

If an image is smaller than 1024×1024, it will be centered on a 1024×1024 canvas and the remaining space will be filled with pure black padding.

For example, a 400×600 image will remain 400×600 and be placed in the center of a 1024×1024 canvas.

For true resolution enhancement, use a dedicated upscaling workflow before running this utility. Diffusion-based upscalers are generally recommended when preparing images for AI training datasets, as they can add detail more naturally than basic interpolation methods.


