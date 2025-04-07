from PIL import Image
from pathlib import Path


def create_story_image(photo_path: Path, size=(720, 1280)) -> Path:
    # Open the input image
    with Image.open(photo_path) as im:
        # Resize to 1x1 to get dominant color
        small_im = im.resize((1, 1))
        dominant_color = small_im.getpixel((0, 0))

        # Create the background image
        bg = Image.new("RGB", size, dominant_color)

        # Resize the main image to fit nicely in the center (e.g., max 600x600)
        max_img_size = (600, 600)
        im.thumbnail(max_img_size, Image.ANTIALIAS)

        # Calculate position to center the image
        bg_width, bg_height = size
        img_width, img_height = im.size
        position = ((bg_width - img_width) // 2, (bg_height - img_height) // 2)

        # Paste the image on the background
        bg.paste(im, position)

        # Save result
        result_path = photo_path.parent / f"story_{photo_path.stem}.jpg"
        bg.save(result_path)

        return result_path