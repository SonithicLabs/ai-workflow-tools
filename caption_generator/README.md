# Caption Generator

## Overview

Caption Generator is a lightweight utility designed to accelerate AI dataset preparation workflows by automatically generating missing caption files for image datasets.

The tool scans a selected folder for supported image formats and creates corresponding `.txt` caption files for any images that do not already have one. Each generated caption file is populated with a user-defined tag string.

This utility is particularly useful when creating training datasets where a common identifier, trigger word, or baseline caption must be applied consistently across an entire image set.


## Features

- Automatically creates missing caption files

- Supports JPG, JPEG, and PNG image formats

- Prevents overwriting existing captions

- Simple drag-and-drop workflow

- No installation or command-line knowledge required


## Setup

Before running the tool, open:

```
`Caption\_generator.py`
```

Locate the following line:

```
`target\_tag = "\[ENTER TAGS HERE\]"`
```

Replace the placeholder text with the tag or caption string you wish to apply to the dataset.

Example:

```
`target\_tag = "SS\_Christina, woman, blonde hair"`
```

Save the file after making your changes.


## Usage

1. Edit the `target\_tag` value inside `Caption\_generator.py`

2. Save the file

3. Drag and drop a folder containing images onto `Caption\_generator\_dragdrop.bat`

4. The utility will:

   - Scan the folder for supported image files

   - Create missing `.txt` caption files

   - Populate each new caption file with the specified tag string

Existing caption files are left unchanged.


## Example

Dataset Folder Before:

```
`image001.jpg`

`image002.jpg`

`image003.jpg`
```

Dataset Folder After:

```
`image001.jpg`

`image001.txt`


`image002.jpg`

`image002.txt`


`image003.jpg`

`image003.txt`
```

Each generated caption file contains the user-defined tag string configured in `target\_tag`.


## Why This Tool Exists

Creating hundreds or thousands of caption files manually is repetitive, time-consuming, and prone to human error.

This utility was developed to automate a common dataset preparation task and reduce setup time from hours of manual work to a matter of seconds.

