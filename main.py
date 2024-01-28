from tkinter import Tk, filedialog as fd
from watermark import *


def input_text(text_var):
    watermark_object.text = text_var
    canvas_box.watermark_update()


def change_opacity(value):
    watermark_object.change_opacity(value)
    canvas_box.watermark_update()


def change_color(value):
    watermark_object.change_color(value)
    canvas_box.watermark_update()


def rotate_watermark(action):
    watermark_object.rotate(action)
    canvas_box.watermark_update()


def move_watermark(action):
    watermark_object.change_position(action)
    canvas_box.watermark_update()


def change_size(action):
    watermark_object.change_size(action, size_widget.get_value())
    canvas_box.watermark_update()


def open_file():
    image_file = fd.askopenfilename(
        filetypes=[
            ("jpeg", ".jpg .jpeg"),
            ("png", ".png"),
            ("bitmap", "bmp"),
            ("gif", ".gif"),
        ]
    )

    canvas_box.load_photo(image_file)


# Create the main window
window = Tk()
window.geometry("810x525")
window.title("My Watermarking App")


# Create Watermark object and WatermarkingBox widget
watermark_object = Watermark(window)
canvas_box = WatermarkingBox(window, watermark_object)
canvas_box.grid(row=0, column=0, padx=20, rowspan=6)

# Create various widgets for interacting with the watermark
TextBoxWidget(window, input_text).grid(row=0, column=1, pady=20)
ColorandOpacityWidget(window, change_color, change_opacity).grid(
    row=1, column=1, pady=20
)
RotateWidget(window, rotate_watermark).grid(row=2, column=1, pady=20)
PositionWidget(window, move_watermark).grid(row=3, column=1, pady=20)
size_widget = SizeWidget(window, change_size)
size_widget.grid(row=4, column=1, pady=20)

# Create FileHandling widget for opening and saving files
FileHandling(window, open_file, canvas_box.save).grid(row=5, column=1, pady=20)

window.mainloop()
