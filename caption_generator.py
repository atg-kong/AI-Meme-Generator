"""
Caption Generator Module
Generates humorous meme captions using LLM (OpenAI GPT or HuggingFace models)
"""

import openai
from typing import List, Dict, Optional
from config import config


class CaptionGenerator:
    """Generates meme captions using various LLM providers"""

    def __init__(self, provider: str = None, model: str = None):
        """
        Initialize the caption generator

        Args:
            provider: LLM provider ('openai', 'huggingface', 'local')
            model: Specific model to use
        """
        self.provider = provider or config.LLM_PROVIDER
        self.model = model or config.LLM_MODEL

        # Initialize OpenAI if using that provider
        if self.provider == 'openai':
            if not config.OPENAI_API_KEY:
                raise ValueError("OpenAI API key not configured. Please set OPENAI_API_KEY in .env file")
            openai.api_key = config.OPENAI_API_KEY

    def generate_caption(
        self,
        topic: str,
        template_name: Optional[str] = None,
        style: str = "funny",
        num_lines: int = 2
    ) -> Dict[str, str]:
        """
        Generate a meme caption based on the topic

        Args:
            topic: The subject/topic for the meme
            template_name: Optional template name for context-aware generation
            style: Style of humor ('funny', 'sarcastic', 'wholesome', 'dark')
            num_lines: Number of caption lines (typically 1 or 2)

        Returns:
            Dictionary with 'top_text' and 'bottom_text' keys
        """
        if self.provider == 'openai':
            return self._generate_with_openai(topic, template_name, style, num_lines)
        elif self.provider == 'huggingface':
            return self._generate_with_huggingface(topic, template_name, style, num_lines)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def _generate_with_openai(
        self,
        topic: str,
        template_name: Optional[str],
        style: str,
        num_lines: int
    ) -> Dict[str, str]:
        """Generate caption using OpenAI's API"""

        # Construct a detailed prompt for better caption generation
        template_context = f" for the '{template_name}' meme template" if template_name else ""

        prompt = f"""You are a creative meme caption writer. Generate a {style} meme caption about "{topic}"{template_context}.

Requirements:
- The caption should be humorous and relatable
- Use {num_lines} line(s) of text
- Keep each line under 60 characters
- Use internet/meme culture references when appropriate
- Be concise and punchy

Format your response as:
TOP: <top text>
BOTTOM: <bottom text>

If only 1 line is needed, leave BOTTOM empty."""

        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a witty meme caption generator who understands internet humor and meme culture."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=config.MAX_CAPTION_TOKENS,
                temperature=config.TEMPERATURE
            )

            # Parse the response
            caption_text = response.choices[0].message.content.strip()
            return self._parse_caption_response(caption_text, num_lines)

        except Exception as e:
            print(f"Error generating caption with OpenAI: {e}")
            # Return fallback caption
            return {
                'top_text': topic.upper(),
                'bottom_text': 'SOMETHING WENT WRONG' if num_lines == 2 else ''
            }

    def _generate_with_huggingface(
        self,
        topic: str,
        template_name: Optional[str],
        style: str,
        num_lines: int
    ) -> Dict[str, str]:
        """Generate caption using HuggingFace models (placeholder for future implementation)"""
        # TODO: Implement HuggingFace integration
        print("HuggingFace provider not yet implemented, using fallback")
        return {
            'top_text': topic.upper(),
            'bottom_text': 'HUGGINGFACE COMING SOON' if num_lines == 2 else ''
        }

    def _parse_caption_response(self, response_text: str, num_lines: int) -> Dict[str, str]:
        """
        Parse the LLM response into top and bottom text

        Args:
            response_text: Raw response from LLM
            num_lines: Expected number of lines

        Returns:
            Dictionary with 'top_text' and 'bottom_text'
        """
        top_text = ""
        bottom_text = ""

        # Try to parse structured format (TOP: / BOTTOM:)
        lines = response_text.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('TOP:'):
                top_text = line.replace('TOP:', '').strip()
            elif line.startswith('BOTTOM:'):
                bottom_text = line.replace('BOTTOM:', '').strip()

        # If structured format not found, try to split by newline
        if not top_text and not bottom_text:
            non_empty_lines = [l.strip() for l in lines if l.strip()]
            if non_empty_lines:
                top_text = non_empty_lines[0]
                if num_lines == 2 and len(non_empty_lines) > 1:
                    bottom_text = non_empty_lines[1]

        # Final fallback
        if not top_text:
            top_text = response_text[:60].strip()

        return {
            'top_text': top_text,
            'bottom_text': bottom_text
        }

    def generate_multiple_captions(
        self,
        topic: str,
        template_name: Optional[str] = None,
        count: int = 3
    ) -> List[Dict[str, str]]:
        """
        Generate multiple caption variations

        Args:
            topic: The subject/topic for the meme
            template_name: Optional template name
            count: Number of variations to generate

        Returns:
            List of caption dictionaries
        """
        captions = []
        styles = ['funny', 'sarcastic', 'wholesome']

        for i in range(count):
            style = styles[i % len(styles)]
            caption = self.generate_caption(topic, template_name, style)
            captions.append(caption)

        return captions


# Example usage
if __name__ == "__main__":
    # Test the caption generator
    try:
        generator = CaptionGenerator()

        # Test single caption generation
        caption = generator.generate_caption(
            topic="working from home",
            template_name="Drake Hotline Bling",
            style="funny"
        )

        print("Generated Caption:")
        print(f"Top: {caption['top_text']}")
        print(f"Bottom: {caption['bottom_text']}")

    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("\nPlease set up your .env file with required API keys.")
        print("Copy .env.example to .env and add your credentials.")
