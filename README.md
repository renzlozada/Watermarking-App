# Watermarking App with Tkinter

This is a simple watermarking application built using Tkinter, allowing users to add watermarks to images with customizable properties.

## Features

- Load an image file.
- Apply a text watermark with customizable properties:
  - Text input
  - Color selection
  - Opacity adjustment
  - Rotation
  - Positioning
  - Font size adjustment
- Save the watermarked image.

## Dependencies

- Tkinter: Standard GUI toolkit for Python.
- watermark module: Custom module containing classes and functions for watermarking.

## Usage

1. **Run the Script**
    ```python
    python main.py
    ```

2. **Open an Image**
   - Use the "Open" button to load an image.
   
3. **Customize Watermark**
   - Enter the desired watermark text.
   - Adjust color, opacity, rotation, position, and font size using the provided widgets.

4. **Save Watermarked Image**
   - Save the watermarked image using the "Save" button.

## File Structure

- **main.py:** Main script for the watermarking application.
- **watermark.py:** Module containing watermark-related classes and functions.
- **/images:** Directory containing icons for open and save buttons.
- **/font:** Directory containing font files.

## Widgets

- **TextBoxWidget:** Enter and apply watermark text.
- **ColorandOpacityWidget:** Select color and adjust opacity.
- **RotateWidget:** Rotate the watermark clockwise or counter-clockwise.
- **PositionWidget:** Change the position of the watermark.
- **SizeWidget:** Select the font size of the watermark.
- **FileHandling:** Open and save image files.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
