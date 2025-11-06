"""
Template Selector Module
Selects appropriate meme templates from dataset or Imgflip API
"""

import json
import random
import requests
from typing import List, Dict, Optional
from config import config


class TemplateSelector:
    """Handles meme template selection and management"""

    def __init__(self, use_local_dataset: bool = True):
        """
        Initialize the template selector

        Args:
            use_local_dataset: Whether to use local dataset or Imgflip API
        """
        self.use_local_dataset = use_local_dataset
        self.templates = []

        if use_local_dataset:
            self._load_local_templates()
        else:
            self._fetch_imgflip_templates()

    def _load_local_templates(self):
        """Load templates from local memes.json dataset"""
        try:
            with open(config.MEMES_DATASET_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Extract template information
            self.templates = []
            for template in data:
                # Fix URL format
                url = template.get('base_img', '')
                if url.startswith('//'):
                    url = 'https:' + url
                elif not url.startswith('http'):
                    url = 'https://' + url

                self.templates.append({
                    'id': template.get('id'),
                    'name': template.get('name'),
                    'url': url,
                    'width': template.get('width'),
                    'height': template.get('height'),
                    'box_count': template.get('text_box', 2),
                    'examples': template.get('generated_memes', [])[:3]  # Keep top 3 examples
                })

            print(f"Loaded {len(self.templates)} templates from local dataset")

        except FileNotFoundError:
            print(f"Local dataset not found at {config.MEMES_DATASET_PATH}")
            print("Falling back to Imgflip API")
            self._fetch_imgflip_templates()
        except Exception as e:
            print(f"Error loading local templates: {e}")
            self.templates = []

    def _fetch_imgflip_templates(self):
        """Fetch templates from Imgflip API"""
        try:
            response = requests.get(config.IMGFLIP_GET_MEMES_URL, timeout=10)
            response.raise_for_status()

            data = response.json()
            if data.get('success'):
                memes = data['data']['memes']
                self.templates = [
                    {
                        'id': meme['id'],
                        'name': meme['name'],
                        'url': meme['url'],
                        'width': meme['width'],
                        'height': meme['height'],
                        'box_count': meme['box_count'],
                        'examples': []
                    }
                    for meme in memes
                ]
                print(f"Fetched {len(self.templates)} templates from Imgflip API")
            else:
                print("Failed to fetch templates from Imgflip API")
                self.templates = []

        except Exception as e:
            print(f"Error fetching Imgflip templates: {e}")
            self.templates = []

    def get_random_template(self) -> Optional[Dict]:
        """
        Get a random meme template

        Returns:
            Template dictionary or None if no templates available
        """
        if not self.templates:
            return None
        return random.choice(self.templates)

    def get_template_by_name(self, name: str) -> Optional[Dict]:
        """
        Find a template by name (case-insensitive, partial match)

        Args:
            name: Template name to search for

        Returns:
            Template dictionary or None if not found
        """
        name_lower = name.lower()

        # First try exact match
        for template in self.templates:
            if template['name'].lower() == name_lower:
                return template

        # Then try partial match
        for template in self.templates:
            if name_lower in template['name'].lower():
                return template

        return None

    def get_template_by_id(self, template_id: int) -> Optional[Dict]:
        """
        Find a template by ID

        Args:
            template_id: Template ID

        Returns:
            Template dictionary or None if not found
        """
        for template in self.templates:
            if template['id'] == template_id:
                return template
        return None

    def search_templates(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for templates matching a query

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of matching templates
        """
        query_lower = query.lower()
        matches = [
            template for template in self.templates
            if query_lower in template['name'].lower()
        ]
        return matches[:limit]

    def get_popular_templates(self, limit: int = 20) -> List[Dict]:
        """
        Get most popular meme templates

        Args:
            limit: Number of templates to return

        Returns:
            List of popular templates
        """
        # Return first N templates (they're generally ordered by popularity)
        return self.templates[:limit]

    def get_template_for_topic(self, topic: str) -> Optional[Dict]:
        """
        Intelligently select a template based on topic

        Args:
            topic: The meme topic/subject

        Returns:
            Appropriate template or random template
        """
        topic_lower = topic.lower()

        # Define topic to template mappings
        topic_keywords = {
            'success': ['Success Kid', 'First World Problems'],
            'fail': ['Bad Luck Brian', 'Disaster Girl'],
            'comparison': ['Drake Hotline Bling', 'Distracted Boyfriend', 'Two Buttons'],
            'decision': ['Two Buttons', 'Drake Hotline Bling', 'Daily Struggle'],
            'confusion': ['Confused Nick Young', 'Jackie Chan WTF'],
            'wisdom': ['Ancient Aliens', 'Roll Safe Think About It'],
            'debate': ['Change My Mind', 'They\'re The Same Picture'],
            'panic': ['Bike Fall', 'This Is Fine'],
            'work': ['This Is Fine', 'Waiting Skeleton'],
            'programming': ['Two Buttons', 'Drake Hotline Bling'],
            'relationship': ['Distracted Boyfriend', 'Drake Hotline Bling']
        }

        # Find matching category
        for keyword, template_names in topic_keywords.items():
            if keyword in topic_lower:
                for template_name in template_names:
                    template = self.get_template_by_name(template_name)
                    if template:
                        return template

        # Fallback to random popular template
        popular = self.get_popular_templates(30)
        return random.choice(popular) if popular else self.get_random_template()

    def list_all_templates(self) -> List[str]:
        """
        Get list of all template names

        Returns:
            List of template names
        """
        return [template['name'] for template in self.templates]

    def get_template_info(self, template: Dict) -> str:
        """
        Get formatted information about a template

        Args:
            template: Template dictionary

        Returns:
            Formatted template information string
        """
        info = f"Template: {template['name']}\n"
        info += f"ID: {template['id']}\n"
        info += f"Dimensions: {template['width']}x{template['height']}\n"
        info += f"Text boxes: {template['box_count']}\n"
        info += f"URL: {template['url']}"
        return info


# Example usage
if __name__ == "__main__":
    # Test the template selector
    selector = TemplateSelector(use_local_dataset=True)

    print(f"\nTotal templates loaded: {len(selector.templates)}")

    # Test random template
    random_template = selector.get_random_template()
    if random_template:
        print("\n--- Random Template ---")
        print(selector.get_template_info(random_template))

    # Test search
    print("\n--- Search for 'Drake' ---")
    results = selector.search_templates("Drake")
    for template in results:
        print(f"- {template['name']}")

    # Test topic-based selection
    print("\n--- Template for 'programming' ---")
    template = selector.get_template_for_topic("programming decision making")
    if template:
        print(selector.get_template_info(template))
