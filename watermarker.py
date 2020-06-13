import sys
import os
from PIL import Image, ImageDraw, ImageFont
import subprocess
import argparse


class Watermarker(object):
    """Add text watermark to an image"""

    def __init__(self, watermark_text, img_path, brightness=160, alpha=150, fontsize=0):
        self.watermark_text = watermark_text
        self.img_path = img_path
        self.brightness = brightness
        self.alpha = alpha
        self.vertical_spacing = 4
        self.horizontal_spacing = 1.4
        self.fontsize = fontsize

    def save(self, save_path=None):
        if not save_path:
            save_path = self.img_path

        loaded_image = None
        try:
            loaded_image = Image.open(self.img_path).convert("RGBA")

            width, height = loaded_image.size

            print("width:", width)
            print("height:", height)

            diag = (width ** 2 + height ** 2) ** (0.5)
            print("diag:", diag)

            if not self.fontsize:
                self.fontsize = int(min(width, height) / 20)
            print("fontsize:", self.fontsize)

            txt = Image.new("RGBA", (int(diag), int(diag)), (255, 255, 255, 0))
            draw = ImageDraw.Draw(txt)
            font = ImageFont.truetype("resources/FiraCode-Bold.ttf", self.fontsize)
            text_size = font.getsize(self.watermark_text)
            print("text_size:", text_size)
            text_width, text_height = text_size

            start_coords = (50, 50)
            coords = (start_coords[0], start_coords[1])
            print(int(diag / text_width))
            print(int(diag / text_height))

            print("Adding watermark to image...")

            for i in range(int(diag / text_height)):
                # print(i)
                for j in range(int(diag / text_width)):
                    draw.text(
                        coords,
                        self.watermark_text,
                        font=font,
                        fill=(
                            self.brightness,
                            self.brightness,
                            self.brightness,
                            self.alpha,
                        ),
                    )
                    coords = (
                        coords[0] + text_width * self.horizontal_spacing,
                        coords[1],
                    )

                coords = (
                    text_width / 2 + start_coords[0]
                    if (i % 2 == 0)
                    else start_coords[0],
                    coords[1] + text_height * self.vertical_spacing,
                )

            w = txt.rotate(45)
            loaded_image.paste(w, (-int(height / 6), -int(width / 6)), mask=w)

            print("Saving...")
            if not self.img_path.endswith("png"):
                loaded_image = loaded_image.convert("RGB")
            loaded_image.save(save_path)
            print("Done!")

            subprocess.run(["open", save_path], check=True)
        finally:
            if loaded_image:
                loaded_image.close()


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("image_path", help="Path to the image to add watermark to")
    parser.add_argument("watermark_text", help="Watermark text to overlay in the image")
    parser.add_argument(
        "-o", "--output", help="Specify output path to save edited image"
    )
    parser.add_argument(
        "-a",
        "--alpha",
        help="Specify alpha of the watermark text",
        default=150,
        type=int,
    )
    parser.add_argument(
        "-b",
        "--brightness",
        help="Specify brightness of the watermark text",
        default=160,
        type=int,
    )
    parser.add_argument(
        "-f",
        "--fontsize",
        help="Specify a font size for the watermark text. By default, size is adjusted according to image size.",
        default=0,
        type=int,
    )
    options = parser.parse_args(args[1:])
    if not options.output:
        options.output = "_watermarked".join(os.path.splitext(options.image_path))

    Watermarker(
        options.watermark_text,
        options.image_path,
        brightness=options.brightness,
        alpha=options.alpha,
        fontsize=options.fontsize
    ).save(options.output)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
