# lf_box/image_utils.py

from io import BytesIO
from PIL import Image

def resize_image(image_bytes, max_size):
    """Resizes an image to a maximum width or height while maintaining aspect ratio."""
    image = Image.open(BytesIO(image_bytes))
    width, height = image.size

    if width > height:
        new_width = max_size
        new_height = int(height * (max_size / width))
    else:
        new_height = max_size
        new_width = int(width * (max_size / height))

    image = image.resize((new_width, new_height), Image.LANCZOS)

    # Convert the image to RGB if it's not already
    if image.mode not in ("L", "RGB", "RGBA"):
        image = image.convert("RGB")

    output = BytesIO()
    image.save(output, format="JPEG")  # You can change the format if needed
    return output.getvalue()