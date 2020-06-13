# Watermarker

Add text watermark to an image.

## Dependencies
* Python >= 3.6
* [Pillow](https://pillow.readthedocs.io/en/stable/)


## Usage

```bash
python watermarker.py <image_path> <watermark_text>
```


#### Options:
* `--output` Specify output path to save edited image. (Default save path is the source image suffixed by `_watermarked`).
* `--alpha` Specify alpha of the watermark text
* `--brightness` Specify brightness of the watermark text


### Example
```bash
python watermarker.py my_image.png "Hello There!" -o watermarked_image.png
```

![watermarked image](https://github.com/apff/watermarker/raw/master/watermarked_image.png)