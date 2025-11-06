# AI Meme Generator
Generate context‑aware memes based on user input or trending topics.

## 📌 Project Overview
We build an application that:
- Takes a user prompt (free text) or fetches a trending topic.
- Uses an LLM (e.g., GPT‑4 / Llama 3) to craft a humorous caption appropriate for a meme template.
- Selects (or generates) a meme image template from a library (e.g., Imgflip API).
- Places the generated caption onto the template.
- Delivers the final meme image to the user.

## 🧰 Tools & Technologies
- Language Model: GPT (OpenAI) or Hugging Face model.
- Meme Template API: Imgflip API.
- Trending topic fetcher: News API / Reddit API.
- Web front‑end: React / Next.js / Thunkable.
- Back‑end: Python (Flask/FastAPI) or Node.js.
- Storage: SQLite or Firestore.
- Image generation: Stable Diffusion, DALL·E.
- Deployment: Heroku / Vercel / AWS Lambda.

## 📂 Dataset & Template Library
- Imgflip API for templates (`/get_memes`).
- Kaggle dataset: ImgFlip‑Scraped Memes Caption Dataset.
- HuggingFace dataset: MemeFact Templates.

## 🛠 Architecture & Workflow
User input → Generate caption → Choose template → Overlay caption → Output meme image.

## 📝 Setup Instructions
### Install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install openai flask requests pillow
```

### Generate caption (example)
```python
import openai

openai.api_key = "YOUR_KEY"

def generate_caption(topic):
    prompt = f"Create a funny meme caption about {topic}."
    resp = openai.ChatCompletion.create(
        model="gpt‑4‑turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=30
    )
    return resp.choices[0].message.content.strip()
```

### Meme creation (example)
```python
import requests

r = requests.get("https://api.imgflip.com/get_memes")
template = r.json()["data"]["memes"][0]

params = {
    "template_id": template["id"],
    "username": "YOUR_IMGFLIP_USERNAME",
    "password": "YOUR_IMGFLIP_PASSWORD",
    "text0": "When you finish your project",
    "text1": "but forgot to push to git"
}
r2 = requests.post("https://api.imgflip.com/caption_image", params=params)
print(r2.json()["data"]["url"])
```

## ✅ Deliverables
- README.md (this file)
- Source code
- Dataset folder
- Demo (web interface or mobile)
- Report/presentation

## 📚 References
- Imgflip API: https://imgflip.com/api
- Kaggle Dataset: https://www.kaggle.com/datasets/abhishtagatya/imgflipscraped-memes-caption-dataset
- MemeFact Dataset: https://huggingface.co/datasets/sergiogpinto/memefact-templates
