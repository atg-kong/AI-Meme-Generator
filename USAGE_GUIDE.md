# AI Meme Generator - Complete Usage Guide

## Table of Contents
1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Running the Application](#running-the-application)
4. [Web Interface](#web-interface)
5. [API Usage](#api-usage)
6. [Programmatic Usage](#programmatic-usage)
7. [Example Scripts](#example-scripts)
8. [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for downloading images and API calls)
- OpenAI API key

### Step 1: Clone and Setup

```bash
# Navigate to project directory
cd AI-Meme-Generator

# Run automated setup
chmod +x setup.sh
./setup.sh
```

Or manually:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Extract dataset
unzip memes.json.zip
```

## Configuration

### Step 1: Create .env file

```bash
cp .env.example .env
```

### Step 2: Edit .env file

```bash
# Required Configuration
OPENAI_API_KEY=sk-your-actual-openai-api-key

# Optional Configuration
IMGFLIP_USERNAME=your_username
IMGFLIP_PASSWORD=your_password

# App Settings (defaults are fine)
FLASK_ENV=development
PORT=5000
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo
```

### Getting an OpenAI API Key

1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API keys section
4. Create a new API key
5. Copy and paste into your .env file

**Important:** Keep your API key secure and never commit it to version control!

## Running the Application

### Start the Web Server

```bash
# Activate virtual environment
source venv/bin/activate

# Run the application
python app.py
```

You should see:
```
==============================================================
🎨 AI Meme Generator
==============================================================
Templates loaded: 100
LLM Provider: openai
Output directory: /path/to/generated_memes
==============================================================

 * Running on http://0.0.0.0:5000
```

### Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

## Web Interface

### Generating a Meme

1. **Enter Topic**: Type what your meme should be about
   - Examples: "working from home", "debugging code", "Monday mornings"

2. **Choose Template** (Optional):
   - Leave blank for automatic selection
   - Or type a template name (e.g., "Drake Hotline Bling")

3. **Select Humor Style**:
   - Funny: General humor
   - Sarcastic: Witty, sarcastic tone
   - Wholesome: Positive, feel-good
   - Dark: Dark humor

4. **Click "Generate Meme"**

5. **View Result**:
   - See your generated meme
   - View the caption text
   - Download the image

### Tips for Better Results

- **Be specific**: "debugging at 3am" vs "programming"
- **Use relatable topics**: Daily life situations work best
- **Try different styles**: Same topic, different humor styles
- **Experiment with templates**: Some templates work better for certain topics

## API Usage

### Health Check

```bash
curl http://localhost:5000/api/health
```

Response:
```json
{
  "status": "healthy",
  "components": {
    "caption_generator": true,
    "template_selector": true,
    "meme_creator": true
  },
  "templates_loaded": 100
}
```

### Generate Meme

```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "working from home",
    "style": "funny"
  }'
```

Response:
```json
{
  "success": true,
  "meme_url": "/generated_memes/meme_20240101_120000.jpg",
  "caption": {
    "top_text": "WORKING FROM HOME",
    "bottom_text": "PAJAMAS ALL DAY EVERY DAY"
  },
  "template": {
    "name": "Success Kid",
    "url": "https://i.imgflip.com/...",
    "id": 61544
  }
}
```

### Generate with Specific Template

```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "choosing between options",
    "template_name": "Drake Hotline Bling",
    "style": "sarcastic"
  }'
```

### Get Available Templates

```bash
# Get all templates
curl http://localhost:5000/api/templates

# Search for specific templates
curl "http://localhost:5000/api/templates?search=Drake&limit=5"
```

### Generate Caption Only

```bash
curl -X POST http://localhost:5000/api/caption \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "online meetings",
    "template_name": "Distracted Boyfriend"
  }'
```

## Programmatic Usage

### Basic Example

```python
from caption_generator import CaptionGenerator
from template_selector import TemplateSelector
from meme_creator import MemeCreator

# Initialize
caption_gen = CaptionGenerator()
template_sel = TemplateSelector(use_local_dataset=True)
meme_creator = MemeCreator()

# Generate meme
topic = "debugging code"
template = template_sel.get_template_for_topic(topic)
caption = caption_gen.generate_caption(topic, template['name'])

output = meme_creator.create_meme(
    template_url=template['url'],
    top_text=caption['top_text'],
    bottom_text=caption['bottom_text']
)

print(f"Meme saved to: {output}")
```

### Using Specific Template

```python
# Find specific template
template = template_sel.get_template_by_name("Drake Hotline Bling")

if template:
    print(f"Found: {template['name']}")
    print(f"URL: {template['url']}")
    print(f"Text boxes: {template['box_count']}")
```

### Generate Multiple Variations

```python
# Generate 5 variations
captions = caption_gen.generate_multiple_captions(
    topic="working from home",
    count=5
)

for i, caption in enumerate(captions, 1):
    print(f"\nVariation {i}:")
    print(f"  Top: {caption['top_text']}")
    print(f"  Bottom: {caption['bottom_text']}")
```

### Search Templates

```python
# Search for templates
results = template_sel.search_templates("Drake", limit=5)

for template in results:
    print(f"- {template['name']}")
```

### Different Humor Styles

```python
styles = ['funny', 'sarcastic', 'wholesome', 'dark']

for style in styles:
    caption = caption_gen.generate_caption(
        topic="Monday mornings",
        style=style
    )
    print(f"\n{style.upper()}:")
    print(f"  {caption['top_text']}")
    print(f"  {caption['bottom_text']}")
```

## Example Scripts

The project includes `example_usage.py` with various examples:

### Run All Examples

```bash
# Show help
python example_usage.py

# Run specific example
python example_usage.py 1  # Basic generation
python example_usage.py 2  # Specific template
python example_usage.py 3  # Multiple variations
python example_usage.py 4  # Search templates
python example_usage.py 5  # Different styles
```

### Interactive Mode

```bash
python example_usage.py interactive
```

This provides an interactive CLI where you can:
- Enter topics
- Choose templates
- Generate and save memes
- See results immediately

Example session:
```
Enter meme topic: working from home
Template name (press Enter for auto-select): Drake Hotline Bling
Using template: Drake Hotline Bling
Generating caption...
  Top: GOING TO THE OFFICE
  Bottom: WORKING IN PAJAMAS

Create this meme? (y/n): y
Creating meme...
✓ Meme saved to: generated_memes/meme_20240101_120000.jpg
```

## Troubleshooting

### Common Issues

#### 1. "OpenAI API key not configured"

**Problem:** API key not set or incorrect

**Solution:**
```bash
# Check .env file exists
ls -la .env

# Edit and add your key
nano .env

# Ensure key starts with 'sk-'
OPENAI_API_KEY=sk-your-actual-key
```

#### 2. "Templates not loading"

**Problem:** memes.json file missing

**Solution:**
```bash
# Extract dataset
unzip memes.json.zip

# Verify file exists
ls -lh memes.json
```

#### 3. "Module not found" errors

**Problem:** Dependencies not installed

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### 4. "Failed to download image"

**Problem:** Network issues or invalid URL

**Solution:**
- Check internet connection
- Some older template URLs may be outdated
- Try a different template

#### 5. Font rendering issues

**Problem:** System fonts not available

**Solution:**
The app will automatically fall back to default fonts. For better results:

```bash
# Install Liberation fonts (Linux)
sudo apt-get install fonts-liberation

# Or use system fonts (will work with defaults)
```

#### 6. "Port 5000 already in use"

**Problem:** Another service using port 5000

**Solution:**
```bash
# Change port in .env
PORT=8000

# Or kill the other process
lsof -ti:5000 | xargs kill -9
```

### Debug Mode

Enable detailed logging:

```bash
# In .env file
FLASK_DEBUG=1
FLASK_ENV=development
```

Then check console output for detailed error messages.

### Getting Help

If you encounter issues:

1. Check the error message carefully
2. Verify all configuration in .env
3. Ensure virtual environment is activated
4. Check API key has credits
5. Review the console output for clues

### API Rate Limits

OpenAI has rate limits. If you hit them:

1. Wait a few minutes
2. Check your OpenAI dashboard for usage
3. Consider upgrading your OpenAI plan
4. Reduce the frequency of requests

## Advanced Usage

### Custom LLM Provider

Modify `config.py` to add support for other providers:

```python
# In config.py
LLM_PROVIDER = 'huggingface'  # or 'local'
```

### Custom Template Selection Logic

Modify `template_selector.py` to customize template matching:

```python
# Add your own topic keywords
topic_keywords = {
    'your_topic': ['Template Name 1', 'Template Name 2']
}
```

### Custom Image Processing

Modify `meme_creator.py` to customize:
- Font sizes
- Text positioning
- Outline width
- Colors

### Production Deployment

For production use:

```bash
# Use Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Or with more workers
gunicorn -w 8 --timeout 120 -b 0.0.0.0:5000 app:app
```

## Best Practices

1. **API Key Security**
   - Never commit .env to git
   - Use environment variables in production
   - Rotate keys regularly

2. **Rate Limiting**
   - Be mindful of API costs
   - Cache results when possible
   - Implement rate limiting for production

3. **Error Handling**
   - Always check API responses
   - Have fallback templates
   - Log errors for debugging

4. **Performance**
   - Generate memes asynchronously for scale
   - Cache popular templates
   - Optimize image processing

---

For more information, see the main README.md or visit the project repository.
