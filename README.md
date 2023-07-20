# GifToFrames - Python App

GifToFrames is a Python application that allows you to convert GIF files into individual frames and create sprite sheets from those frames. You can also export the frames as individual PNG files.

## Requirements

- Python 3
- Tkinter
- Pillow (Python Imaging Library)

## Installation

1. Make sure you have Python 3 installed on your system.
2. Install the required packages using pip:
   ```
   pip install Pillow
   ```
3. You have two options to obtain the GifToFrames application files:
   - **Option 1: Clone the Repository (Recommended)**:
     ```
     git clone https://github.com/Huntrox/GifToFrames.git
     cd GifToFrames
     ```
   - **Option 2: Download the Files**:
     - Download the two Python files, main.py and GifToFrames.py, and save them in the same directory.

## Usage

To use the GifToFrames app, run the `main.py` script from your terminal or command prompt:

```
python main.py
```

A GUI window will appear with the application interface.

### Functions

1. **Open**: Click the "Open" option in the File menu to select a GIF file from your computer. The GIF file will be loaded, and its frames will be displayed as thumbnails on the interface.

2. **Export**: After loading a GIF file, the "Export" option in the File menu will become enabled. Clicking on "Export" will create individual PNG files for each frame of the GIF. The exported PNG files will be saved in the `output` directory within the same directory as the GIF file.

3. **Export Sheet**: This option creates a sprite sheet from the frames of the loaded GIF. The sprite sheet will be saved as a PNG file in the `output` directory.

4. **About**: Click on the "About" option in the Help menu to display information about the GifToFrames application.

## Notes

- The application supports GIF files only. Make sure your file ends with `.gif`.
- The application allows you to preview the frames of the loaded GIF as thumbnails.
- The `output` directory will be automatically created to store the exported PNG files and sprite sheets.

## License

GifToFrames is open-source software under the [MIT License](https://opensource.org/licenses/MIT). You are free to use, modify, and distribute the code as per the terms of the license.
