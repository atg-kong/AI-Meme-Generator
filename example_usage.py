"""
Example Usage Scripts for AI Meme Generator
Demonstrates how to use the various modules
"""

import sys
from config import config
from caption_generator import CaptionGenerator
from template_selector import TemplateSelector
from meme_creator import MemeCreator


def example_1_basic_meme():
    """Example 1: Generate a basic meme"""
    print("\n" + "="*60)
    print("Example 1: Basic Meme Generation")
    print("="*60)

    try:
        # Initialize components
        caption_gen = CaptionGenerator()
        template_sel = TemplateSelector(use_local_dataset=True)
        meme_creator = MemeCreator()

        # Generate caption
        topic = "Monday mornings"
        print(f"\nTopic: {topic}")

        caption = caption_gen.generate_caption(topic)
        print(f"Caption generated:")
        print(f"  Top: {caption['top_text']}")
        print(f"  Bottom: {caption['bottom_text']}")

        # Select template
        template = template_sel.get_template_for_topic(topic)
        print(f"\nTemplate selected: {template['name']}")

        # Create meme
        output_path = meme_creator.create_meme(
            template_url=template['url'],
            top_text=caption['top_text'],
            bottom_text=caption['bottom_text']
        )

        print(f"\n✓ Meme created: {output_path}")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure you have set up your .env file with API keys.")


def example_2_specific_template():
    """Example 2: Use a specific template"""
    print("\n" + "="*60)
    print("Example 2: Using Specific Template")
    print("="*60)

    try:
        caption_gen = CaptionGenerator()
        template_sel = TemplateSelector(use_local_dataset=True)
        meme_creator = MemeCreator()

        # Find specific template
        template_name = "Drake Hotline Bling"
        template = template_sel.get_template_by_name(template_name)

        if not template:
            print(f"Template '{template_name}' not found")
            return

        print(f"\nTemplate: {template['name']}")

        # Generate caption with template context
        topic = "coding with AI vs coding manually"
        caption = caption_gen.generate_caption(
            topic=topic,
            template_name=template['name']
        )

        print(f"\nTopic: {topic}")
        print(f"Caption generated:")
        print(f"  Top: {caption['top_text']}")
        print(f"  Bottom: {caption['bottom_text']}")

        # Create meme
        output_path = meme_creator.create_meme(
            template_url=template['url'],
            top_text=caption['top_text'],
            bottom_text=caption['bottom_text']
        )

        print(f"\n✓ Meme created: {output_path}")

    except Exception as e:
        print(f"\n✗ Error: {e}")


def example_3_multiple_variations():
    """Example 3: Generate multiple caption variations"""
    print("\n" + "="*60)
    print("Example 3: Multiple Caption Variations")
    print("="*60)

    try:
        caption_gen = CaptionGenerator()

        topic = "working from home"
        print(f"\nTopic: {topic}")
        print("\nGenerating 3 variations...\n")

        captions = caption_gen.generate_multiple_captions(topic, count=3)

        for i, caption in enumerate(captions, 1):
            print(f"Variation {i}:")
            print(f"  Top: {caption['top_text']}")
            print(f"  Bottom: {caption['bottom_text']}")
            print()

    except Exception as e:
        print(f"\n✗ Error: {e}")


def example_4_search_templates():
    """Example 4: Search and explore templates"""
    print("\n" + "="*60)
    print("Example 4: Template Search")
    print("="*60)

    template_sel = TemplateSelector(use_local_dataset=True)

    # Show statistics
    print(f"\nTotal templates loaded: {len(template_sel.templates)}")

    # Search for templates
    search_query = "Drake"
    print(f"\nSearching for '{search_query}':")
    results = template_sel.search_templates(search_query, limit=5)

    for template in results:
        print(f"  - {template['name']} (ID: {template['id']})")

    # Show popular templates
    print("\nTop 10 popular templates:")
    popular = template_sel.get_popular_templates(limit=10)

    for i, template in enumerate(popular, 1):
        print(f"  {i}. {template['name']}")


def example_5_custom_styles():
    """Example 5: Different humor styles"""
    print("\n" + "="*60)
    print("Example 5: Different Humor Styles")
    print("="*60)

    try:
        caption_gen = CaptionGenerator()
        topic = "online meetings"

        styles = ['funny', 'sarcastic', 'wholesome']

        print(f"\nTopic: {topic}\n")

        for style in styles:
            caption = caption_gen.generate_caption(
                topic=topic,
                style=style
            )
            print(f"{style.upper()} style:")
            print(f"  Top: {caption['top_text']}")
            print(f"  Bottom: {caption['bottom_text']}")
            print()

    except Exception as e:
        print(f"\n✗ Error: {e}")


def interactive_mode():
    """Interactive mode for generating memes"""
    print("\n" + "="*60)
    print("Interactive Meme Generator")
    print("="*60)

    try:
        caption_gen = CaptionGenerator()
        template_sel = TemplateSelector(use_local_dataset=True)
        meme_creator = MemeCreator()

        while True:
            print("\n" + "-"*60)
            topic = input("\nEnter meme topic (or 'quit' to exit): ").strip()

            if topic.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if not topic:
                print("Please enter a topic")
                continue

            # Optional template selection
            template_input = input("Template name (press Enter for auto-select): ").strip()

            if template_input:
                template = template_sel.get_template_by_name(template_input)
                if not template:
                    print(f"Template '{template_input}' not found. Using auto-select.")
                    template = template_sel.get_template_for_topic(topic)
            else:
                template = template_sel.get_template_for_topic(topic)

            print(f"\nUsing template: {template['name']}")
            print("Generating caption...")

            # Generate caption
            caption = caption_gen.generate_caption(
                topic=topic,
                template_name=template['name']
            )

            print(f"  Top: {caption['top_text']}")
            print(f"  Bottom: {caption['bottom_text']}")

            # Ask if user wants to create the meme
            create = input("\nCreate this meme? (y/n): ").strip().lower()

            if create == 'y':
                print("Creating meme...")
                output_path = meme_creator.create_meme(
                    template_url=template['url'],
                    top_text=caption['top_text'],
                    bottom_text=caption['bottom_text']
                )
                print(f"✓ Meme saved to: {output_path}")

    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye!")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def main():
    """Main function to run examples"""
    print("\n" + "="*60)
    print("AI Meme Generator - Example Usage")
    print("="*60)

    if len(sys.argv) > 1:
        example = sys.argv[1]

        examples = {
            '1': example_1_basic_meme,
            '2': example_2_specific_template,
            '3': example_3_multiple_variations,
            '4': example_4_search_templates,
            '5': example_5_custom_styles,
            'interactive': interactive_mode,
            'i': interactive_mode
        }

        if example in examples:
            examples[example]()
        else:
            print(f"Unknown example: {example}")
            print_usage()
    else:
        print_usage()


def print_usage():
    """Print usage information"""
    print("\nUsage: python example_usage.py [example_number]")
    print("\nAvailable examples:")
    print("  1 - Basic meme generation")
    print("  2 - Using specific template")
    print("  3 - Multiple caption variations")
    print("  4 - Search and explore templates")
    print("  5 - Different humor styles")
    print("  i - Interactive mode")
    print("\nExample:")
    print("  python example_usage.py 1")
    print("  python example_usage.py interactive")


if __name__ == "__main__":
    main()
