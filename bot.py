import os, json, requests, subprocess, random, time
from io import BytesIO

BOT_TOKEN = os.environ['BOT_TOKEN']
CHANNEL_ID = os.environ['CHANNEL_ID']
STABILITY_API_KEY = os.environ.get('STABILITY_API_KEY')
INDEX_FILE = "last_index.json"
MAX_CAPTION_LENGTH = 900

def build_image_prompt():
    # আপনার বোল্ড প্রম্পট (কোনো পরিবর্তন নেই)
    scenes = [
        "A Bangladeshi woman in a thin saree, pallu lifted, blouse unbuttoned halfway, heavy breasts pressing against lace bra, panty visible through wet saree, kneeling on bed, cinematic lighting, intense eyes",
        "Woman in a saree, blouse completely open, black bra cupping full breasts, saree falling off one shoulder, standing near window, rainy evening, panty line visible, sensual mood",
        # ... (আপনার সব scenes এখানে কপি করুন) ...
        "Woman in shorts and a tank top, bending forward to pick up something, top slipping, one breast almost exposed, panty waistband showing, natural outdoor lighting",
    ]
    scene = random.choice(scenes)
    colors = random.choice(["warm colors, gold and red tones", "cool colors, blue and silver tones", "pastel colors, soft pink and lavender"])
    lighting = random.choice(["sunset light, golden hour glow", "night time, lantern light", "rainy evening, soft focus", "morning light, dreamy"])
    camera = random.choice(["shot on 50mm lens, bokeh", "cinematic anamorphic", "close-up macro", "wide storytelling shot"])
    uid = f"uid:{random.randint(100000,999999)}_{random.randint(100000,999999)}"
    prompt = f"{scene}, {colors}, {lighting}, {camera}, photorealistic, adult vibe, sensual, tasteful, {uid}"
    return prompt[:400]

def fetch_stability_image(prompt):
    if not STABILITY_API_KEY:
        print("❌ Stability API key not set!")
        return None

    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "text_prompts": [{"text": prompt}],
        "cfg_scale": 7,
        "height": 1024,
        "width": 1024,
        "samples": 1,
        "steps": 30,
    }
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=90)
        if resp.status_code == 200:
            data = resp.json()
            if "artifacts" in data and len(data["artifacts"]) > 0:
                img_b64 = data["artifacts"][0]["base64"]
                import base64
                return BytesIO(base64.b64decode(img_b64)).read()
        print(f"❌ Stability API error: {resp.status_code} - {resp.text[:200]}")
    except Exception as e:
        print(f"❌ Stability image gen failed: {e}")
    return None

# ... (বাকি কোড: পোস্ট লোড, ইনডেক্স, পাঠানোর ফাংশন, ক্যাপশন ভাগ করে পাঠানো ইত্যাদি আগের মতোই)
# শুধু ইমেজ জেনারেশন কল হবে: image_bytes = fetch_stability_image(prompt)

# ---------- টেলিগ্রামে পাঠানোর ফাংশন ----------
def send_telegram_photo(image_bytes, caption):
    """ছবি পাঠায়, ক্যাপশন খুব লম্বা হলে ছোট করে বাকিটা টেক্সট মেসেজে পাঠায়"""
    url_photo = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    url_text = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    reply_markup = {
        "inline_keyboard": [
            [{"text": "🔗 Join Our List", "url": "https://t.me/addlist/57pQLQQl0Oo1MDk9"}]
        ]
    }

    # ক্যাপশন ভাগ করা
    if len(caption) > MAX_CAPTION_LENGTH:
        first_part = caption[:MAX_CAPTION_LENGTH] + "..."
        remaining = caption[MAX_CAPTION_LENGTH:]
    else:
        first_part = caption
        remaining = None

    files = {"photo": ("image.jpg", image_bytes, "image/jpeg")}
    data = {
        "chat_id": CHANNEL_ID,
        "caption": first_part,
        "parse_mode": "HTML",
        "reply_markup": json.dumps(reply_markup)
    }
    resp = requests.post(url_photo, files=files, data=data, timeout=30).json()
    if not resp.get('ok'):
        print(f"❌ sendPhoto error: {resp}")
        # ছবি ব্যর্থ হলে পুরো ক্যাপশন টেক্সট হিসেবে পাঠাই (ভাগ করে)
        send_telegram_text(caption)
        return False
    else:
        print("✅ Image + caption sent!")

    # বাকি অংশ থাকলে আলাদা টেক্সট হিসেবে পাঠাই
    if remaining:
        send_telegram_text(remaining)
    return True

def send_telegram_text(text):
    """লম্বা টেক্সট প্রয়োজনে ছোট ছোট মেসেজে ভাগ করে পাঠায়"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    reply_markup = {
        "inline_keyboard": [
            [{"text": "🔗 Join Our List", "url": "https://t.me/addlist/57pQLQQl0Oo1MDk9"}]
        ]
    }
    # টেক্সটকে 4096 অক্ষরের কম অংশে ভাগ করি (টেলিগ্রাম মেসেজ সীমা)
    max_msg_len = 4000
    parts = [text[i:i+max_msg_len] for i in range(0, len(text), max_msg_len)]
    for part in parts:
        payload = {
            "chat_id": CHANNEL_ID,
            "text": part,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
            "reply_markup": reply_markup
        }
        resp = requests.post(url, json=payload, timeout=15).json()
        if not resp.get('ok'):
            print(f"❌ Text send error: {resp}")

# ---------- পোস্ট লোড ----------
with open('posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

# ---------- ইনডেক্স ----------
try:
    with open(INDEX_FILE, 'r') as f:
        last_index = json.load(f)
except:
    last_index = -1

next_index = (last_index + 1) % len(posts) if posts else 0
post = posts[next_index]
text = post['text']

# ---------- ইমেজ জেনারেট ----------
print("🎨 Generating bold adult vibe cinematic image...")
prompt = build_image_prompt()
image_bytes = fetch_pollinations_image(prompt)

# ---------- পাঠানো ----------
if image_bytes:
    send_telegram_photo(image_bytes, text)
else:
    print("⚠️ Image generation failed – sending text only.")
    send_telegram_text(text)

# ---------- ইনডেক্স সেভ ও গিট পুশ ----------
with open(INDEX_FILE, 'w') as f:
    json.dump(next_index, f)

# গিট কমিট (ক্যাশ যাতে কাজ করে)
try:
    subprocess.run(["git", "config", "user.name", "GitHub Actions"], check=True)
    subprocess.run(["git", "config", "user.email", "actions@github.com"], check=True)
    subprocess.run(["git", "add", INDEX_FILE], check=True)
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"], capture_output=True)
    if diff.returncode != 0:
        subprocess.run(["git", "commit", "-m", "Update last index"], check=True)
        subprocess.run(["git", "pull", "--rebase", "origin", "main"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("✅ Index committed and pushed")
    else:
        print("ℹ️  No change in index")
except subprocess.CalledProcessError as e:
    print(f"⚠️ Git error (push may have failed): {e}")
