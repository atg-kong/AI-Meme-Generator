"""
AI Meme Generator - Demo Version
Simplified version for demonstrations without requiring API keys
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from datetime import datetime

from config import config
from template_selector import TemplateSelector
from meme_creator import MemeCreator
from demo_mode import DemoModeGenerator

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Initialize components with demo mode
try:
    demo_caption_gen = DemoModeGenerator()  # Use demo mode instead of real API
    template_selector = TemplateSelector(use_local_dataset=True)
    meme_creator = MemeCreator()
    print("✓ Demo mode initialized successfully")
    print(f"✓ {len(template_selector.templates)} templates loaded")
    print("✓ Using pre-generated captions (no API key required)")
except Exception as e:
    print(f"✗ Error initializing components: {e}")
    demo_caption_gen = None
    template_selector = None
    meme_creator = None


@app.route('/')
def index():
    """Render the main web interface"""
    return render_template('index.html')


@app.route('/api/generate', methods=['POST'])
def generate_meme():
    """Generate a meme in demo mode"""
    try:
        # Validate components
        if not all([demo_caption_gen, template_selector, meme_creator]):
            return jsonify({
                'success': False,
                'error': 'System components not initialized'
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

        # Step 2: Generate caption using demo mode
        caption = demo_caption_gen.generate_caption(topic)

        # Step 3: Create meme
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
            },
            'demo_mode': True
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
    """Get list of available templates"""
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
            'count': len(templates),
            'demo_mode': True
        })

    except Exception as e:
        print(f"Error fetching templates: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/demo-topics', methods=['GET'])
def get_demo_topics():
    """Get list of pre-loaded demo topics"""
    try:
        if not demo_caption_gen:
            return jsonify({
                'success': False,
                'error': 'Demo mode not initialized'
            }), 500

        topics = demo_caption_gen.get_demo_topics()

        return jsonify({
            'success': True,
            'topics': topics,
            'count': len(topics)
        })

    except Exception as e:
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
        'mode': 'demo',
        'components': {
            'demo_caption_generator': demo_caption_gen is not None,
            'template_selector': template_selector is not None,
            'meme_creator': meme_creator is not None
        },
        'templates_loaded': len(template_selector.templates) if template_selector else 0,
        'demo_topics': len(demo_caption_gen.get_demo_topics()) if demo_caption_gen else 0
    })


if __name__ == '__main__':
    # Ensure directories exist
    config.ensure_directories()

    # Print startup information
    print("\n" + "="*60)
    print("🎨 AI Meme Generator - DEMO MODE")
    print("="*60)
    print("⚡ Quick Demo Features:")
    print(f"   • {len(template_selector.templates) if template_selector else 0} meme templates loaded")
    print(f"   • {len(demo_caption_gen.get_demo_topics()) if demo_caption_gen else 0} pre-generated topics")
    print("   • No API key required")
    print("   • Instant meme generation")
    print("="*60)
    print("🌐 Open: http://localhost:5000")
    print("⚠️  Press Ctrl+C to stop")
    print("="*60 + "\n")

    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=config.PORT,
        debug=False  # Disable debug in demo
    )
