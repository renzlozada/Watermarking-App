from tkinter import (
    Button,
    Entry,
    Frame,
    Label,
    ttk,
    Image,
    StringVar,
    messagebox,
    Scale,
    PhotoImage,
    filedialog as fd,
)

from tkinter.colorchooser import askcolor
import PIL
from PIL import ImageTk, Image, ImageDraw, ImageFont
import os


class TextBoxWidget(Frame):
    """
    A widget for entering and applying watermark text.
    """

    def __init__(self, frame, action):
        super().__init__(frame)
        Label(self, text="Watermark Text").grid(row=0, column=0)
        self.text_var = StringVar()
        Entry(self, textvariable=self.text_var).grid(row=0, column=1)
        Button(self, text="Apply", command=lambda: action(self.text_var.get())).grid(
            row=0, column=2
        )


class ColorandOpacityWidget(Frame):
    """
    A widget for selecting color and adjusting opacity.
    """

    def __init__(self, frame, color_select, action):
        super().__init__(frame)
        color_button = Button(
            self,
            text="Color",
            command=lambda: color_select(askcolor(title="Tkinter Color Chooser")[1]),
        )
        color_button.grid(row=0, column=0)
        Label(self, text="Opacity").grid(row=0, column=2)
        self.opacity_slider = Scale(
            self,
            from_=0,
            to=255,
            orient="horizontal",
            command=lambda value: action(value),
        )
        self.opacity_slider.grid(row=0, column=3)


class RotateWidget(Frame):
    """
    A widget for rotating the watermark clockwise or counter-clockwise.
    """

    def __init__(self, frame, action):
        super().__init__(frame)
        Label(self, text="Rotate").grid(row=0, column=0, padx=10)
        self.clockwise = Button(self, text="↻", command=lambda: action("right"))
        self.clockwise.grid(row=0, column=1)
        self.counterclockwise = Button(self, text="↺", command=lambda: action("left"))
        self.counterclockwise.grid(row=0, column=2, padx=10)


class PositionWidget(Frame):
    """
    A widget for changing the position of the watermark.
    """

    def __init__(self, frame, action):
        super().__init__(frame)
        Label(self, text="Position").grid(row=0, column=1, pady=5)
        buttons = [
            {"text": "▲", "row": 1, "column": 1, "direction": "up"},
            {"text": "◀", "row": 2, "column": 0, "direction": "left"},
            {"text": "▶", "row": 2, "column": 2, "direction": "right"},
            {"text": "▼", "row": 3, "column": 1, "direction": "down"},
        ]

        for button in buttons:
            bttn = Button(
                self,
                text=button["text"],
                width=1,
                command=lambda direction=button["direction"]: action(direction),
            )
            bttn.grid(row=button["row"], column=button["column"])


class SizeWidget(Frame):
    """
    A widget for selecting the font size of the watermark.
    """

    def __init__(self, frame, action):
        super().__init__(frame)
        Label(self, text="Font Size: ").grid(row=0, column=0, padx=8)
        self.size_dropdown = ttk.Combobox(
            self, values=[i for i in range(10, 200, 4)], width=4
        )
        self.size_dropdown.current(10)
        self.size_dropdown.bind("<<ComboboxSelected>>", action)
        self.size_dropdown.grid(row=0, column=1)

    def get_value(self):
        """
        Returns the font size selected in the dropdown.
        """
        """Returns the font size selected in the dropdown"""
        return self.size_dropdown.get()


class FileHandling(Frame):
    """
    A widget for handling opening and saving files.
    """

    def __init__(self, frame, open_file, save_file):
        super().__init__(frame)
        self.open_icon = PhotoImage(file="images/Open.png")
        self.save_icon = PhotoImage(file="images/Save.png")
        self.open_button = Button(
            self,
            image=self.open_icon,
            text=" Open ",
            compound="left",
            command=open_file,
        )
        self.open_button.grid(row=0, column=0, columnspan=2, padx=10)
        self.save_button = Button(
            self,
            image=self.save_icon,
            text=" Save ",
            compound="left",
            command=save_file,
        )
        self.save_button.grid(row=0, column=2, columnspan=2, padx=10)


class Watermark:
    """
    Class representing a watermark with customizable properties.
    """

    def __init__(self, frame):
        self.parent = frame
        self.font_size = 50
        self.opacity = 25
        self.color = (255, 255, 255, self.opacity)
        self.rotation = 0
        self.x = 50
        self.y = 50
        self.text = ""

    def change_color(self, color=None):
        """
        Changes color of the watermark.
        Passes on HEX Code which will be converted automatically by winfo_rgb from Frame
        """
        if color == None:
            list_color = list(self.color)[:3]
        else:
            list_color = list(self.parent.winfo_rgb(color))

        list_color.append(self.opacity)
        self.color = tuple(list_color)

    def change_size(self, event, size):
        """Changes the font_size of the watermark"""
        self.font_size = int(size)

    def change_opacity(self, value):
        """
        Changes the opacity of the watermark
        Drag down the slider from 0 to 255. 0 being invisible, while 255 being opaque
        """
        self.opacity = int(value)
        self.change_color()

    def rotate(self, direction):
        """
        Rotates the watermark clockwise or counter-clockwise
        """
        if direction == "left":
            if self.rotation == 355:
                self.rotation = 0
            else:
                self.rotation += 5
        else:
            if self.rotation == 0:
                self.rotation = 355
            else:
                self.rotation -= 5

    def change_position(self, direction):
        if direction == "up":
            self.y -= 10
        elif direction == "down":
            self.y += 10
        elif direction == "left":
            self.x -= 10
        elif direction == "right":
            self.x += 10


class WatermarkingBox(Label):
    """
    A widget for displaying and applying a watermark to an image.
    """

    def __init__(self, frame, watermark):
        super().__init__(frame)
        self.watermark = watermark  # from Watermark class passed to Watermarking box
        self.image = Image.new(size=(640, 480), mode="RGBA", color="gray")
        self.photo = ImageTk.PhotoImage(self.image)
        self.configure(image=self.photo, padx=5, pady=5)
        self.save_reference = None

    def load_photo(self, path):
        # Loads the photo in the label widget. acting as a canvas
        try:
            self.image = Image.open(path).convert("RGBA")
            self.photo = ImageTk.PhotoImage(self.image)
            self.configure(image=self.photo, padx=5, pady=5)
        except PIL.UnidentifiedImageError:
            messagebox.showerror("Invalid image", f"{path} is not a valid image file.")

    def watermark_update(self):
        """
        Updates the watermark on the displayed image.
        """
        image = self.image.resize(
            (640, int(640 * (self.image.height / self.image.width))), Image.LANCZOS
        )

        txt = Image.new("RGBA", image.size)
        d = ImageDraw.Draw(txt, "RGBA")
        font = ImageFont.FreeTypeFont(
            "font/Roboto-Regular.ttf", size=self.watermark.font_size
        )
        d = ImageDraw.Draw(txt, "RGBA")

        d.text(
            xy=(0, 0), text=self.watermark.text, fill=(self.watermark.color), font=font
        )
        starting_width = txt.width
        starting_height = txt.height

        txt = txt.rotate(self.watermark.rotation, expand=True)

        offset_x = int((txt.width - starting_width) / 2)
        offset_y = int((txt.height - starting_height) / 2)
        image.paste(
            txt, (self.watermark.x - offset_x, self.watermark.y - offset_y), txt
        )
        self.photo = ImageTk.PhotoImage(image)
        self.composite_image = image
        self.configure(image=self.photo)
        self.save_reference = image

    def save(self):
        """
        Combines the watermark text with the full-size image and saves file
        """
        image = self.image.copy()

        # ratio of the displayed image to the full size image
        resize_ratio = image.width / 640

        # create the transparent watermark
        txt = Image.new("RGBA", image.size)
        d = ImageDraw.Draw(txt, "RGBA")
        resized_font = int(self.watermark.font_size * resize_ratio)
        font = ImageFont.FreeTypeFont("font/Roboto-Regular.ttf", size=resized_font)
        d = ImageDraw.Draw(txt, "RGBA")

        d.text(
            xy=(0, 0), text=self.watermark.text, fill=(self.watermark.color), font=font
        )

        # rotate the watermark
        starting_width = txt.width
        starting_height = txt.height
        txt = txt.rotate(self.watermark.rotation, expand=True)

        # relocate the watermark after rotation
        offset_x = int((txt.width - starting_width) / 2)
        offset_y = int((txt.height - starting_height) / 2)

        x_loc = int(self.watermark.x * resize_ratio - offset_x)
        y_loc = int(self.watermark.y * resize_ratio - offset_y)
        image.paste(txt, (x_loc, y_loc), txt)

        file_path = fd.asksaveasfilename(
            confirmoverwrite=True,
            defaultextension="png",
            filetypes=[("jpeg", ".jpg"), ("png", ".png")],
        )
        if file_path is not None:
            if os.path.splitext(file_path)[1] == ".jpg":
                image = image.convert("RGB")
            image.save(fp=file_path)
