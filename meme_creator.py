"""
Meme Creator Module
Handles image download, text overlay, and meme generation
"""

import io
import os
import requests
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, Optional, Tuple
from datetime import datetime
from config import config


class MemeCreator:
    """Creates memes by overlaying text on templates"""

    def __init__(self):
        """Initialize the meme creator"""
        config.ensure_directories()
        self.output_dir = config.GENERATED_MEMES_DIR

    def create_meme(
        self,
        template_url: str,
        top_text: str = "",
        bottom_text: str = "",
        output_filename: Optional[str] = None
    ) -> str:
        """
        Create a meme by overlaying text on a template image

        Args:
            template_url: URL of the meme template image
            top_text: Text for the top of the meme
            bottom_text: Text for the bottom of the meme
            output_filename: Optional custom filename (without path)

        Returns:
            Path to the generated meme image
        """
        try:
            # Download template image
            image = self._download_image(template_url)

            # Add text overlays
            if top_text:
                image = self._add_text(image, top_text, position='top')
            if bottom_text:
                image = self._add_text(image, bottom_text, position='bottom')

            # Generate output filename if not provided
            if not output_filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"meme_{timestamp}.jpg"

            # Save the meme
            output_path = os.path.join(self.output_dir, output_filename)
            image.save(output_path, 'JPEG', quality=95)

            print(f"Meme created successfully: {output_path}")
            return output_path

        except Exception as e:
            print(f"Error creating meme: {e}")
            raise

    def create_meme_with_imgflip(
        self,
        template_id: str,
        top_text: str = "",
        bottom_text: str = ""
    ) -> Optional[str]:
        """
        Create a meme using Imgflip's API (requires credentials)

        Args:
            template_id: Imgflip template ID
            top_text: Text for the top
            bottom_text: Text for the bottom

        Returns:
            URL of the generated meme or None if failed
        """
        if not config.IMGFLIP_USERNAME or not config.IMGFLIP_PASSWORD:
            print("Imgflip credentials not configured")
            return None

        try:
            params = {
                'template_id': template_id,
                'username': config.IMGFLIP_USERNAME,
                'password': config.IMGFLIP_PASSWORD,
                'text0': top_text,
                'text1': bottom_text
            }

            response = requests.post(config.IMGFLIP_CAPTION_URL, data=params, timeout=15)
            response.raise_for_status()

            data = response.json()
            if data.get('success'):
                meme_url = data['data']['url']
                print(f"Meme created with Imgflip: {meme_url}")
                return meme_url
            else:
                print(f"Imgflip API error: {data.get('error_message', 'Unknown error')}")
                return None

        except Exception as e:
            print(f"Error creating meme with Imgflip: {e}")
            return None

    def _download_image(self, url: str) -> Image.Image:
        """
        Download an image from URL

        Args:
            url: Image URL

        Returns:
            PIL Image object
        """
        # Ensure URL has protocol
        if url.startswith('//'):
            url = 'https:' + url

        response = requests.get(url, timeout=15)
        response.raise_for_status()

        image = Image.open(io.BytesIO(response.content))
        return image.convert('RGB')

    def _add_text(
        self,
        image: Image.Image,
        text: str,
        position: str = 'top'
    ) -> Image.Image:
        """
        Add text overlay to an image with meme-style formatting

        Args:
            image: PIL Image object
            text: Text to add
            position: 'top' or 'bottom'

        Returns:
            Modified PIL Image object
        """
        draw = ImageDraw.Draw(image)
        img_width, img_height = image.size

        # Calculate font size based on image dimensions
        font_size = int(img_height / 10)
        font = self._get_font(font_size)

        # Wrap text to fit image width
        wrapped_text = self._wrap_text(text, font, img_width - 20)

        # Calculate text position
        text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        x = (img_width - text_width) / 2
        if position == 'top':
            y = img_height * 0.05  # 5% from top
        else:  # bottom
            y = img_height * 0.95 - text_height  # 5% from bottom

        # Draw text with outline for better visibility
        self._draw_text_with_outline(
            draw, (x, y), wrapped_text, font,
            fill_color='white',
            outline_color='black',
            outline_width=2
        )

        return image

    def _get_font(self, size: int) -> ImageFont.FreeTypeFont:
        """
        Get a font for text rendering

        Args:
            size: Font size

        Returns:
            ImageFont object
        """
        # Try to use Impact font (classic meme font)
        font_paths = [
            '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
            '/System/Library/Fonts/Supplemental/Impact.ttf',
            'C:\\Windows\\Fonts\\Impact.ttf',
            '/Library/Fonts/Impact.ttf'
        ]

        for font_path in font_paths:
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue

        # Fallback to default font
        return ImageFont.load_default()

    def _wrap_text(self, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> str:
        """
        Wrap text to fit within max_width

        Args:
            text: Text to wrap
            font: Font being used
            max_width: Maximum width in pixels

        Returns:
            Wrapped text with newlines
        """
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = font.getbbox(test_line)
            width = bbox[2] - bbox[0]

            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        return '\n'.join(lines)

    def _draw_text_with_outline(
        self,
        draw: ImageDraw.ImageDraw,
        position: Tuple[float, float],
        text: str,
        font: ImageFont.FreeTypeFont,
        fill_color: str = 'white',
        outline_color: str = 'black',
        outline_width: int = 2
    ):
        """
        Draw text with an outline for better visibility

        Args:
            draw: ImageDraw object
            position: (x, y) position tuple
            text: Text to draw
            font: Font to use
            fill_color: Text fill color
            outline_color: Outline color
            outline_width: Outline width in pixels
        """
        x, y = position

        # Draw outline
        for adj_x in range(-outline_width, outline_width + 1):
            for adj_y in range(-outline_width, outline_width + 1):
                if adj_x != 0 or adj_y != 0:
                    draw.multiline_text(
                        (x + adj_x, y + adj_y),
                        text,
                        font=font,
                        fill=outline_color,
                        align='center'
                    )

        # Draw text
        draw.multiline_text(
            (x, y),
            text,
            font=font,
            fill=fill_color,
            align='center'
        )


# Example usage
if __name__ == "__main__":
    # Test the meme creator
    creator = MemeCreator()

    # Example: Create a meme using Drake template
    template_url = "https://i.imgflip.com/30b1gx.jpg"
    top_text = "MANUALLY ADDING TEXT TO IMAGES"
    bottom_text = "USING AI MEME GENERATOR"

    try:
        output_path = creator.create_meme(
            template_url=template_url,
            top_text=top_text,
            bottom_text=bottom_text
        )
        print(f"\nMeme saved to: {output_path}")
    except Exception as e:
        print(f"Failed to create meme: {e}")
