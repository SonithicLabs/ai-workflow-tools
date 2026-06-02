# Image Mirroring Utility

## Overview

Image Mirroring Utility is a lightweight dataset augmentation tool designed to increase dataset size by generating horizontally mirrored copies of existing images.

The utility scans a folder for supported image formats, creates a left-to-right mirrored version of each image, and saves the mirrored copy alongside the original file.

This approach can be particularly useful when working with limited datasets where increasing representation and variation is more important than maintaining exact real-world asymmetry.


## Features

- Generates horizontally mirrored image copies

- Preserves original images

- Supports:

  - JPG

  - JPEG

  - PNG

  - WEBP

- Processes entire folders automatically

- Simple drag-and-drop workflow

- Ideal for rapid dataset augmentation


## Usage

1. Place images inside a folder.

2. Drag and drop the folder onto:

```
`Image\_Mirroring\_dragdrop.bat`
```

3. The utility will:

   - Scan the folder for supported image formats

   - Create a mirrored version of each image

   - Save the mirrored copy alongside the original image


## Example

Before:

```
`image001.jpg`

`image002.jpg`

`image003.jpg`
```

After:

```
`image001.jpg`

`image001B.jpg`


`image002.jpg`

`image002B.jpg`


`image003.jpg`

`image003B.jpg`
```


## Important Considerations

Mirroring is a form of dataset augmentation and may not be appropriate for every use case.

Many real-world datasets contain natural asymmetries, including:

- Hairstyles

- Facial features

- Clothing details

- Logos and text

- Jewelry and accessories

- Environmental elements

Mirroring may introduce variations that do not exist in the original data.

For this reason, the utility is most effective when:

- Dataset size is limited

- Additional representation is desired

- Exact real-world fidelity is not a strict requirement

- The benefits of increased variation outweigh the impact of mirrored asymmetry


## Why This Tool Exists

Acquiring high-quality training images is often the most time-consuming part of dataset creation.

When working with limited datasets, augmentation techniques can provide additional examples that help improve model exposure to different orientations and compositions.

This utility can rapidly increase dataset representation by creating mirrored variants of existing images. The effectiveness of this approach varies based on dataset characteristics and whether left/right asymmetry is important to the target concept. 

