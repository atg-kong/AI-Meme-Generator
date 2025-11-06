"""
AI Meme Generator Flask Application
Main backend API for generating context-aware memes
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from datetime import datetime

from config import config
from caption_generator import CaptionGenerator
from template_selector import TemplateSelector
from meme_creator import MemeCreator


# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize components
try:
    caption_generator = CaptionGenerator()
    template_selector = TemplateSelector(use_local_dataset=True)
    meme_creator = MemeCreator()
    print("✓ All components initialized successfully")
except Exception as e:
    print(f"✗ Error initializing components: {e}")
    caption_generator = None
    template_selector = None
    meme_creator = None


@app.route('/')
def index():
    """Render the main web interface"""
    return render_template('index.html')


@app.route('/api/generate', methods=['POST'])
def generate_meme():
    """
    Generate a meme based on user input

    Request JSON:
    {
        "topic": "working from home",
        "template_name": "Drake Hotline Bling" (optional),
        "style": "funny" (optional),
        "use_imgflip": false (optional)
    }

    Returns:
    {
        "success": true,
        "meme_url": "/generated_memes/meme_20240101_120000.jpg",
        "caption": {
            "top_text": "...",
            "bottom_text": "..."
        },
        "template": {
            "name": "...",
            "url": "..."
        }
    }
    """
    try:
        # Validate components
        if not all([caption_generator, template_selector, meme_creator]):
            return jsonify({
                'success': False,
                'error': 'System components not initialized. Please check configuration.'
            }), 500

        # Parse request
        data = request.get_json()
        topic = data.get('topic', '').strip()

        if not topic:
            return jsonify({
                'success': False,
                'error': 'Topic is required'
            }), 400

        template_name = data.get('template_name')
        style = data.get('style', 'funny')
        use_imgflip = data.get('use_imgflip', False)

        # Step 1: Select template
        if template_name:
            template = template_selector.get_template_by_name(template_name)
            if not template:
                return jsonify({
                    'success': False,
                    'error': f'Template "{template_name}" not found'
                }), 404
        else:
            template = template_selector.get_template_for_topic(topic)

        if not template:
            return jsonify({
                'success': False,
                'error': 'No templates available'
            }), 500

        # Step 2: Generate caption
        caption = caption_generator.generate_caption(
            topic=topic,
            template_name=template['name'],
            style=style,
            num_lines=min(template.get('box_count', 2), 2)
        )

        # Step 3: Create meme
        if use_imgflip and config.IMGFLIP_USERNAME:
            # Use Imgflip API
            meme_url = meme_creator.create_meme_with_imgflip(
                template_id=str(template['id']),
                top_text=caption['top_text'],
                bottom_text=caption['bottom_text']
            )

            if not meme_url:
                # Fallback to local generation
                output_path = meme_creator.create_meme(
                    template_url=template['url'],
                    top_text=caption['top_text'],
                    bottom_text=caption['bottom_text']
                )
                meme_url = f"/generated_memes/{os.path.basename(output_path)}"
        else:
            # Use local generation
            output_path = meme_creator.create_meme(
                template_url=template['url'],
                top_text=caption['top_text'],
                bottom_text=caption['bottom_text']
            )
            meme_url = f"/generated_memes/{os.path.basename(output_path)}"

        # Return success response
        return jsonify({
            'success': True,
            'meme_url': meme_url,
            'caption': caption,
            'template': {
                'name': template['name'],
                'url': template['url'],
                'id': template['id']
            }
        })

    except Exception as e:
        print(f"Error generating meme: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/templates', methods=['GET'])
def get_templates():
    """
    Get list of available templates

    Query params:
    - search: Search query (optional)
    - limit: Number of results (default: 50)

    Returns:
    {
        "success": true,
        "templates": [...]
    }
    """
    try:
        if not template_selector:
            return jsonify({
                'success': False,
                'error': 'Template selector not initialized'
            }), 500

        search_query = request.args.get('search', '').strip()
        limit = int(request.args.get('limit', 50))

        if search_query:
            templates = template_selector.search_templates(search_query, limit=limit)
        else:
            templates = template_selector.get_popular_templates(limit=limit)

        return jsonify({
            'success': True,
            'templates': templates,
            'count': len(templates)
        })

    except Exception as e:
        print(f"Error fetching templates: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/caption', methods=['POST'])
def generate_caption_only():
    """
    Generate a caption without creating the meme

    Request JSON:
    {
        "topic": "working from home",
        "template_name": "Drake Hotline Bling" (optional),
        "style": "funny" (optional)
    }

    Returns:
    {
        "success": true,
        "caption": {
            "top_text": "...",
            "bottom_text": "..."
        }
    }
    """
    try:
        if not caption_generator:
            return jsonify({
                'success': False,
                'error': 'Caption generator not initialized'
            }), 500

        data = request.get_json()
        topic = data.get('topic', '').strip()

        if not topic:
            return jsonify({
                'success': False,
                'error': 'Topic is required'
            }), 400

        template_name = data.get('template_name')
        style = data.get('style', 'funny')

        caption = caption_generator.generate_caption(
            topic=topic,
            template_name=template_name,
            style=style
        )

        return jsonify({
            'success': True,
            'caption': caption
        })

    except Exception as e:
        print(f"Error generating caption: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/generated_memes/<filename>')
def serve_meme(filename):
    """Serve generated meme images"""
    return send_from_directory(config.GENERATED_MEMES_DIR, filename)


@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'components': {
            'caption_generator': caption_generator is not None,
            'template_selector': template_selector is not None,
            'meme_creator': meme_creator is not None
        },
        'templates_loaded': len(template_selector.templates) if template_selector else 0
    })


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    # Ensure directories exist
    config.ensure_directories()

    # Validate configuration
    try:
        config.validate()
    except ValueError as e:
        print(f"\n⚠️  Configuration Warning: {e}")
        print("The app will run but some features may be limited.\n")

    # Print startup information
    print("\n" + "="*60)
    print("🎨 AI Meme Generator")
    print("="*60)
    print(f"Templates loaded: {len(template_selector.templates) if template_selector else 0}")
    print(f"LLM Provider: {config.LLM_PROVIDER}")
    print(f"Output directory: {config.GENERATED_MEMES_DIR}")
    print("="*60 + "\n")

    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=config.PORT,
        debug=config.DEBUG
    )
