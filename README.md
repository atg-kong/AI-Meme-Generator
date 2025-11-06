# 🎨 AI Meme Generator

Generate context-aware memes with AI! Perfect for presentations and demos.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## ⚡ Quick Start (Google Colab - Easiest!)

**No installation needed! Run in your browser:**

1. **Open Google Colab:** https://colab.research.google.com/
2. **Upload notebook:** `AI_Meme_Generator_Colab.ipynb`
3. **Click:** Runtime → Run all
4. **Generate memes!** Use the interactive widgets

That's it! Takes just 1 minute to set up.

---

## 🎯 What It Does

- 🤖 **AI-Powered Captions** - Generates contextually relevant meme text
- 🖼️ **81 Meme Templates** - All popular formats included
- 🎨 **Professional Styling** - Classic meme text overlay
- 📱 **Interactive Interface** - Easy-to-use widgets in Colab
- 📥 **Download Results** - Save your creations

---

## 🚀 Features

### In Google Colab:
✅ Interactive widgets for live generation
✅ Simple generator (just enter topic)
✅ Advanced generator (choose templates)
✅ Batch generator (multiple memes at once)
✅ Template browser (view all 81 templates)
✅ Download as zip file
✅ No API key required (demo mode)

### Example Topics:
- "working from home"
- "debugging code"
- "Monday morning"
- "online meetings"
- "exam tomorrow"

---

## 🏗️ Architecture

```
User Input → Caption Generation → Template Selection → Image Overlay → Meme Output
```

**Core Modules:**
- `caption_generator.py` - AI caption generation
- `template_selector.py` - Smart template matching
- `meme_creator.py` - Image processing & text overlay
- `demo_mode.py` - Pre-generated captions (no API key needed)
- `config.py` - Configuration management

---

## 💻 Local Setup (Optional)

If you want to run locally instead of Colab:

```bash
# Clone repository
git clone https://github.com/atg-kong/AI-Meme-Generator.git
cd AI-Meme-Generator

# Install dependencies
pip install -r requirements.txt

# Extract dataset
unzip memes.json.zip

# Run Flask app
python app.py
```

Open http://localhost:5000

---

## 📊 Dataset

**ImgFlip Memes Dataset:**
- 81 popular meme templates
- Template metadata (dimensions, text boxes)
- Example captions included

Templates include Drake Hotline Bling, Distracted Boyfriend, Two Buttons, Success Kid, This Is Fine, and 76+ more!

---

## 🎓 Perfect for Presentations

### Presentation Flow:

1. Open Colab notebook
2. Run all cells (~1 minute setup)
3. Use widgets to generate memes live
4. Show different templates and styles
5. Let audience suggest topics
6. Download examples

---

## 🎨 Usage Example

```python
from demo_mode import DemoModeGenerator
from template_selector import TemplateSelector
from meme_creator import MemeCreator

# Initialize (demo mode - no API key)
caption_gen = DemoModeGenerator()
template_sel = TemplateSelector(use_local_dataset=True)
meme_creator = MemeCreator()

# Generate meme
topic = "working from home"
template = template_sel.get_template_for_topic(topic)
caption = caption_gen.generate_caption(topic)

meme_path = meme_creator.create_meme(
    template_url=template['url'],
    top_text=caption['top_text'],
    bottom_text=caption['bottom_text']
)
```

---

## 📂 Project Structure

```
AI-Meme-Generator/
├── AI_Meme_Generator_Colab.ipynb  ⭐ Main Colab notebook
├── app.py                          Flask application
├── caption_generator.py            AI caption generation
├── template_selector.py            Template selection
├── meme_creator.py                 Image processing
├── demo_mode.py                    Demo captions
├── config.py                       Configuration
├── requirements.txt                Dependencies
├── memes.json.zip                  Dataset (81 templates)
├── templates/                      Web UI
└── static/                         CSS/JS
```

---

## 🔧 Configuration

For local setup with OpenAI GPT-4:

```bash
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=your_key_here
```

**Note:** Colab demo mode doesn't require API keys!

---

## 🆘 Troubleshooting

**Colab: "Runtime disconnected"**
→ Click Reconnect, run cells again

**Local: "Templates not loading"**
→ Extract `memes.json.zip`

**Local: "API key not configured"**
→ Use demo mode or add OpenAI key to `.env`

---

## ⭐ Quick Tips

1. **For presentations:** Use Google Colab (easiest!)
2. **Practice once** before presenting
3. **Prepare 3-5 topics** that work well
4. **Show the code** to explain your work
5. **Let audience participate** - interactive demos are best!

---

**Made for educational demonstrations and creative fun! 🎨**

**⭐ Star this repo if you find it useful!**
