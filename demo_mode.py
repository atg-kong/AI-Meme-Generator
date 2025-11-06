"""
Demo Mode for AI Meme Generator
Provides pre-generated captions for demonstration without requiring API keys
"""

import random
from typing import Dict, List

# Pre-generated demo captions for various topics
DEMO_CAPTIONS = {
    "working from home": [
        {"top_text": "GOING TO THE OFFICE", "bottom_text": "WORKING IN PAJAMAS"},
        {"top_text": "PROFESSIONAL ON TOP", "bottom_text": "PAJAMAS ON BOTTOM"},
        {"top_text": "COMMUTE: 10 SECONDS", "bottom_text": "FROM BED TO DESK"}
    ],
    "debugging": [
        {"top_text": "FINDING THE BUG", "bottom_text": "IT WAS A MISSING SEMICOLON"},
        {"top_text": "CODE WORKS", "bottom_text": "DON'T KNOW WHY"},
        {"top_text": "DEBUGGING AT 3AM", "bottom_text": "STILL CAN'T FIND THE BUG"}
    ],
    "programming": [
        {"top_text": "COPYING CODE FROM STACKOVERFLOW", "bottom_text": "IT WORKS FIRST TRY"},
        {"top_text": "MY CODE", "bottom_text": "PRODUCTION CODE"},
        {"top_text": "WRITING CODE", "bottom_text": "DEBUGGING CODE"}
    ],
    "monday": [
        {"top_text": "MONDAY MORNING", "bottom_text": "NEED MORE COFFEE"},
        {"top_text": "WEEKEND", "bottom_text": "MONDAY"},
        {"top_text": "IT'S MONDAY", "bottom_text": "EVERYTHING IS FINE"}
    ],
    "coffee": [
        {"top_text": "BEFORE COFFEE", "bottom_text": "AFTER COFFEE"},
        {"top_text": "COFFEE IS LIFE", "bottom_text": "LIFE IS COFFEE"},
        {"top_text": "ONE MORE CUP", "bottom_text": "SAID 5 CUPS AGO"}
    ],
    "online meetings": [
        {"top_text": "YOU'RE ON MUTE", "bottom_text": "STILL ON MUTE"},
        {"top_text": "CAMERA OFF", "bottom_text": "STILL IN BED"},
        {"top_text": "IMPORTANT MEETING", "bottom_text": "COULD HAVE BEEN AN EMAIL"}
    ],
    "exams": [
        {"top_text": "STUDIED ALL SEMESTER", "bottom_text": "FORGOT EVERYTHING"},
        {"top_text": "EXAM IN 5 MINUTES", "bottom_text": "STARTS STUDYING NOW"},
        {"top_text": "EASY EXAM", "bottom_text": "FIRST QUESTION IS IMPOSSIBLE"}
    ],
    "ai": [
        {"top_text": "DOING IT MANUALLY", "bottom_text": "USING AI"},
        {"top_text": "BEFORE AI", "bottom_text": "AFTER AI"},
        {"top_text": "AI WILL HELP", "bottom_text": "AI DID EVERYTHING"}
    ],
    "school": [
        {"top_text": "HOMEWORK DUE TOMORROW", "bottom_text": "STARTS AT 11PM"},
        {"top_text": "TEACHER: ANY QUESTIONS?", "bottom_text": "ME: CONFUSED SILENCE"},
        {"top_text": "WEEKEND PLANS", "bottom_text": "HOMEWORK"}
    ],
    "projects": [
        {"top_text": "PROJECT DEADLINE", "bottom_text": "STARTS PROJECT"},
        {"top_text": "IT WORKS ON MY MACHINE", "bottom_text": "PRODUCTION: ERROR"},
        {"top_text": "ESTIMATED: 2 HOURS", "bottom_text": "ACTUAL: 2 DAYS"}
    ]
}

# Template suggestions for different topics
TOPIC_TEMPLATES = {
    "comparison": ["Drake Hotline Bling", "Distracted Boyfriend", "Expanding Brain"],
    "decision": ["Two Buttons", "Drake Hotline Bling"],
    "confusion": ["Confused Nick Young", "Surprised Pikachu"],
    "disaster": ["This Is Fine", "Disaster Girl"],
    "success": ["Success Kid", "Leonardo Dicaprio Cheers"],
    "failure": ["Bad Luck Brian", "Bike Fall"]
}


class DemoModeGenerator:
    """Provides demo captions without requiring API access"""

    def __init__(self):
        """Initialize demo mode generator"""
        self.demo_captions = DEMO_CAPTIONS

    def generate_caption(self, topic: str, **kwargs) -> Dict[str, str]:
        """
        Generate a demo caption based on topic

        Args:
            topic: The meme topic
            **kwargs: Additional arguments (ignored in demo mode)

        Returns:
            Dictionary with 'top_text' and 'bottom_text'
        """
        topic_lower = topic.lower()

        # Try to find matching pre-generated caption
        for key, captions in self.demo_captions.items():
            if key in topic_lower or topic_lower in key:
                return random.choice(captions)

        # Check for common keywords
        if any(word in topic_lower for word in ['work', 'office', 'home']):
            return random.choice(self.demo_captions['working from home'])
        elif any(word in topic_lower for word in ['bug', 'debug', 'error']):
            return random.choice(self.demo_captions['debugging'])
        elif any(word in topic_lower for word in ['code', 'program', 'developer']):
            return random.choice(self.demo_captions['programming'])
        elif any(word in topic_lower for word in ['meet', 'zoom', 'call']):
            return random.choice(self.demo_captions['online meetings'])
        elif any(word in topic_lower for word in ['exam', 'test', 'study']):
            return random.choice(self.demo_captions['exams'])
        elif any(word in topic_lower for word in ['homework', 'school', 'class']):
            return random.choice(self.demo_captions['school'])
        elif any(word in topic_lower for word in ['project', 'deadline']):
            return random.choice(self.demo_captions['projects'])

        # Generic fallback
        return {
            'top_text': topic.upper()[:50],
            'bottom_text': 'DEMO MODE - ADD API KEY FOR AI CAPTIONS'
        }

    def get_demo_topics(self) -> List[str]:
        """Get list of available demo topics"""
        return list(self.demo_captions.keys())

    def add_demo_caption(self, topic: str, caption: Dict[str, str]):
        """Add a new demo caption"""
        if topic not in self.demo_captions:
            self.demo_captions[topic] = []
        self.demo_captions[topic].append(caption)


# Example usage
if __name__ == "__main__":
    demo = DemoModeGenerator()

    print("🎨 AI Meme Generator - Demo Mode")
    print("=" * 60)
    print("\nAvailable demo topics:")
    for i, topic in enumerate(demo.get_demo_topics(), 1):
        print(f"  {i}. {topic}")

    print("\n" + "=" * 60)
    print("\nGenerating sample captions...\n")

    # Test a few topics
    test_topics = ["working from home", "debugging", "online meetings"]

    for topic in test_topics:
        caption = demo.generate_caption(topic)
        print(f"Topic: {topic}")
        print(f"  Top: {caption['top_text']}")
        print(f"  Bottom: {caption['bottom_text']}")
        print()
