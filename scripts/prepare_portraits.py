#!/usr/bin/env python3
"""Prepare portrait files in place; original full-resolution photos belong elsewhere."""

import argparse
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps

MAX_SIDE = 800
MAX_BYTES = 200 * 1024
FORMATS = {".jpg": "JPEG", ".jpeg": "JPEG", ".png": "PNG", ".webp": "WEBP"}
PORTRAITS = Path("assets/images/people")


def prepare(data, suffix):
    """Return a square, metadata-free portrait within the size budget."""
    image_format = FORMATS[suffix.lower()]
    with Image.open(BytesIO(data)) as source:
        if getattr(source, "n_frames", 1) != 1:
            raise ValueError("Use a still portrait, not an animated image.")
        source.load()
        intrinsic_info = {"jfif", "jfif_version", "jfif_unit", "jfif_density",
                          "progressive", "progression"}
        if image_format == "WEBP":
            intrinsic_info |= {"loop", "background", "timestamp", "duration"}
        if (source.format == image_format and source.width == source.height
                and source.width <= MAX_SIDE and len(data) <= MAX_BYTES
                and source.mode in ("RGB", "L", "P")
                and not source.getexif()
                and not (set(source.info) - intrinsic_info)
                and not getattr(source, "text", {})):
            return data  # Do not repeatedly re-encode already prepared portraits.
        image = ImageOps.exif_transpose(source).convert("RGBA")
        background = Image.new("RGBA", image.size, "white")
        background.alpha_composite(image)
        image = background.convert("RGB")

    side = min(MAX_SIDE, *image.size)
    image = ImageOps.fit(image, (side, side), method=Image.Resampling.LANCZOS)
    image.info.clear()
    while True:
        options = (None, 256, 128, 64) if image_format == "PNG" else (85, 78, 70, 60)
        for setting in options:
            output = BytesIO()
            if image_format == "PNG":
                candidate = image if setting is None else image.quantize(colors=setting)
                candidate.save(output, "PNG", optimize=True)
            elif image_format == "JPEG":
                image.save(output, "JPEG", quality=setting, optimize=True, progressive=True)
            else:
                image.save(output, "WEBP", quality=setting, method=6)
            result = output.getvalue()
            if len(result) <= MAX_BYTES:
                return result
        side = int(side * 0.8)
        if side < 128:
            raise ValueError("Cannot compress this portrait within 200 KiB.")
        image = image.resize((side, side), Image.Resampling.LANCZOS)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("photos", type=Path, nargs="*", help="Defaults to all member portraits")
    args = parser.parse_args()
    paths = args.photos or sorted(p for p in PORTRAITS.iterdir() if p.suffix.lower() in FORMATS)
    for path in paths:
        if path.suffix.lower() not in FORMATS:
            parser.error(f"{path}: use JPG, JPEG, PNG, or WebP")
        try:
            original = path.read_bytes()
            result = prepare(original, path.suffix)
            if result != original:
                path.write_bytes(result)
            print(f"{path}: {len(original) / 1024:.0f} → {len(result) / 1024:.0f} KiB")
        except (OSError, ValueError) as error:
            parser.exit(1, f"{path}: {error}\n")


if __name__ == "__main__":
    main()
