import os, json, requests, subprocess, random, time
from io import BytesIO

BOT_TOKEN = os.environ['BOT_TOKEN']
CHANNEL_ID = os.environ['CHANNEL_ID']
INDEX_FILE = "last_index.json"

# ---------- ইমেজ জেনারেশন সেকশন ----------
def build_image_prompt():
    """প্রতিবার সম্পূর্ণ নতুন, বোল্ড অ্যাডাল্ট ভাইব, সিনেমাটিক রিয়েলিস্টিক ইমেজ প্রম্পট"""
    
    # 🎯 বিশাল দৃশ্যপট – শাড়ি, ব্লাউজ, ব্রা, প্যান্টি, সাজেশন, রোমান্টিক পোজ
    scenes = [
        # ___ শাড়ি আঁচল খোলা, দুধ বোঝা ব্রা, প্যান্টি দেখা ___
        "A Bangladeshi woman in a thin saree, pallu lifted, blouse unbuttoned halfway, heavy breasts pressing against lace bra, panty visible through wet saree, kneeling on bed, cinematic lighting, intense eyes",
        "Woman in a saree, blouse completely open, black bra cupping full breasts, saree falling off one shoulder, standing near window, rainy evening, panty line visible, sensual mood",
        "Close-up of a woman untying her saree knot, blouse hooks open, bra strap slipping, cleavage heavy, soft focus, warm golden light",
        "Woman in a saree, leaning forward, saree pallu slipping, deep cleavage, bra cups visible, panty waistband peeking above petticoat, village hut background, natural light",
        "Side view of a woman in a saree, blouse buttons popped, bra strap fallen, one breast almost spilling out, sweat on skin, hot afternoon light",
        
        # ___ ব্লাউজ খোলা, দুধ বের করা, ব্রা ছাড়া ___
        "A woman sitting on a bed, blouse thrown aside, only a thin bra covering her large breasts, nipples poking through fabric, saree pooled around her waist, dim bedroom light",
        "Woman in a transparent blouse, no bra, nipples dark and visible, saree draped low on waist, navel wet with sweat, standing by a lantern, village night",
        "A woman unbuttoning her blouse while looking back over her shoulder, bra unhooked, breasts free but hidden by her arm, mirror reflection, intimate atmosphere",
        
        # ___ প্যান্টি দেখা, ভেজা দাগ, গুদ থেকে রস ___
        "Woman in a thin white saree, sitting with legs slightly apart, a dark wet patch visible between her thighs, blouse open, bra soaked, embarrassed expression, soft morning light",
        "A woman lifting her saree to reveal her panty, a damp spot clearly visible, fingers touching the wet fabric, biting her lip, village bedroom",
        "Close-up of a woman's navel and lower belly, saree pushed aside, panty soaked through, a trickle of moisture running down inner thigh, dim candlelight, highly suggestive",
        
        # ___ সেক্স পজিশন (কাপড়ে ঢাকা, রোমান্টিক) ___
        "Couple on a bed, woman in a saree lying beneath a man, her legs wrapped around his waist, blouse open, bra visible, man kissing her neck, cinematic, romantic, silhouetted against window light",
        "Woman in a saree sitting on top of a man (cowgirl position), both partially clothed, her pallu trailing, blouse buttons open, heavy breathing, dim lantern light, village bedroom",
        "Man and woman in doggy style, woman on all fours, saree pushed up to her waist, panty pulled aside, man's hand gripping her hip, rainy night outside, soft focus, artistic",
        "Woman leaning against a wall, one leg lifted, man pressed against her, saree disheveled, blouse open, intense eye contact, streetlight through window",
        
        # ___ দরজার ফাঁকে কেউ দেখছে, ধরা পড়ার মুহূর্ত ___
        "A couple in intimate embrace on a bed, suddenly a door creaks open, a shocked face of a family member peeking through the gap, woman clutching saree to her chest, man turning in surprise, cinematic suspense",
        "Woman giving oral pleasure to a man (implied, head in lap), saree pallu fallen, blouse open, suddenly a shadow appears at the door, her wide eyes looking up, man startled, dramatic lighting",
        "A couple in missionary position, woman's saree disheveled, bra visible, man on top, suddenly a door opens a crack, silhouette of a person watching, woman gasps, frozen moment, photorealistic",
        
        # ___ এক্সপ্রেশন, জিভ চাটা, গুদ চাটা সাজেশন ___
        "Woman lying on bed, saree lifted to her waist, panty pulled to the side, a man's head between her thighs (implied cunnilingus), woman arching her back, mouth open in pleasure, soft candlelight, highly artistic",
        "Close-up of a woman's face, eyes half-closed, tongue touching her upper lip, a man's hand on her blouse, bra strap fallen, background blurred, intense erotic tension",
        "Woman sitting on a chair, one leg up, saree hiked, a man kneeling in front of her (implied oral), her head thrown back, hands in his hair, moody red lighting, cinematic",
        
        # ___ দেহের ভাঁজ, ঘাম, ভেজা ত্বক ___
        "Woman in a saree after a bath, wet hair, water droplets on her breasts, thin blouse clinging, nipples erect, saree low on hips, panty string visible, standing near a window, rain outside, soft focus",
        "Close-up of a woman's navel, saree draped low, sweat trickling down, blouse open, bra wet with perspiration, shallow breathing, macro shot, sensual",
        "Woman lying on her stomach, saree untied, blouse off, bare back with a thin chain, dim light, shadow patterns, romantic yet erotic",
        
        # ___ সেক্সি শর্টস, টপ, বোল্ড ___
        "A Bangladeshi girl in tiny shorts and a crop top, sitting on a bed, one leg crossed, panty line visible, cleavage heavy, looking directly at camera, bold expression, village house",
        "Woman in shorts and a tank top, bending forward to pick up something, top slipping, one breast almost exposed, panty waistband showing, natural outdoor lighting",
    ]

    # র‌্যান্ডম সিন নির্বাচন
    scene = random.choice(scenes)

    # 🎨 রঙ প্যালেট
    colors = random.choice([
        "warm colors, gold and red tones",
        "cool colors, blue and silver tones",
        "pastel colors, soft pink and lavender",
        "earthy tones, brown and green",
        "high contrast, black and red accents"
    ])

    # 💡 আলোকসজ্জা ও আবহাওয়া
    lighting = random.choice([
        "sunset light, golden hour glow, long shadows",
        "night time, lantern light, warm shadows, intimate",
        "rainy evening, wet textures, soft focus, cinematic",
        "morning light, soft and dreamy, dust particles",
        "dim candlelight, dramatic shadows, moody atmosphere"
    ])

    # 📷 ক্যামেরা অ্যাঙ্গেল ও ইফেক্ট
    camera = random.choice([
        "shot on 50mm lens, shallow depth of field, bokeh",
        "cinematic lighting, movie still, anamorphic lens",
        "close-up, macro detail, skin texture visible",
        "wide shot, full body, environmental storytelling",
        "soft focus, analog film grain, vintage look"
    ])

    # 🧂 ইউনিক সল্ট – ক্যাশ পুরোপুরি ভেঙে দেয়
    unique_salt = f"uid:{random.randint(100000, 999999)}_{random.randint(100000, 999999)}_{random.randint(100000, 999999)}"

    prompt = f"{scene}, {colors}, {lighting}, {camera}, photorealistic, adult vibe, no explicit nudity, tasteful, {unique_salt}"
    return prompt[:400]  # Pollinations.ai URL length limit


def fetch_pollinations_image(prompt):
    encoded = requests.utils.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}"
    print(f"🎨 Pollinations URL: {url}")

    for attempt in range(3):
        try:
            resp = requests.get(url, timeout=60)
            print(f"   Attempt {attempt+1}: status {resp.status_code}, length {len(resp.content)}")
            if resp.status_code == 200 and 'image' in resp.headers.get('content-type', ''):
                return BytesIO(resp.content).read()
            elif resp.status_code == 503:
                print(f"   Server busy, retrying in 8 sec...")
                time.sleep(8)
            else:
                print(f"   Unexpected status/content-type. Body: {resp.text[:100]}")
                break
        except Exception as e:
            print(f"   Error: {e}")
            break
    return None


# পোস্ট লোড
with open('posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

# শেষ ইনডেক্স পড়া
try:
    with open(INDEX_FILE, 'r') as f:
        last_index = json.load(f)
except:
    last_index = -1

# পরবর্তী ইনডেক্স (সিরিয়াল, সব শেষে আবার প্রথমে)
next_index = (last_index + 1) % len(posts) if posts else 0

# পোস্ট সিলেক্ট
post = posts[next_index]
text = post['text']

# 🔥 ইনলাইন বাটন তৈরি
reply_markup = {
    "inline_keyboard": [
        [
            {"text": "🔗 Join Our List", "url": "https://t.me/addlist/57pQLQQl0Oo1MDk9"}
        ]
    ]
}

# ---------- ইমেজ জেনারেট করা ----------
print("🎨 Generating bold adult vibe cinematic image...")
prompt = build_image_prompt()
image_bytes = fetch_pollinations_image(prompt)

# ---------- টেলিগ্রামে পাঠানো ----------
send_photo_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
send_msg_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

if image_bytes:
    # ছবি পাঠাই
    files = {"photo": ("image.jpg", image_bytes, "image/jpeg")}
    data = {
        "chat_id": CHANNEL_ID,
        "caption": text,
        "parse_mode": "HTML",
        "reply_markup": json.dumps(reply_markup)
    }
    try:
        resp = requests.post(send_photo_url, files=files, data=data, timeout=30).json()
        if resp.get('ok'):
            print("✅ Image + caption posted!")
        else:
            print(f"❌ sendPhoto error: {resp}")
            # fallback টেক্সট
            resp2 = requests.post(send_msg_url, json={
                "chat_id": CHANNEL_ID,
                "text": text,
                "parse_mode": "HTML",
                "disable_web_page_preview": True,
                "reply_markup": reply_markup
            }, timeout=15).json()
            print("✅ Text fallback posted" if resp2.get('ok') else f"❌ Text fallback error: {resp2}")
    except Exception as e:
        print(f"❌ Exception sending photo: {e}")
        # fallback
        requests.post(send_msg_url, json={
            "chat_id": CHANNEL_ID,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
            "reply_markup": reply_markup
        }, timeout=15)
else:
    # ছবি নেই – শুধু টেক্সট
    print("⚠️ Image generation failed – sending text only.")
    resp = requests.post(send_msg_url, json={
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
        "reply_markup": reply_markup
    }, timeout=15).json()
    if resp.get('ok'):
        print("✅ Text posted!")
    else:
        print(f"❌ Text error: {resp}")
        exit(1)

# ইনডেক্স আপডেট ও সেভ
with open(INDEX_FILE, 'w') as f:
    json.dump(next_index, f)

# গিট কমিট ও পুশ (কনফ্লিক্ট এড়াতে pull --rebase সহ)
try:
    subprocess.run(["git", "config", "user.name", "GitHub Actions"], check=True)
    subprocess.run(["git", "config", "user.email", "actions@github.com"], check=True)
    subprocess.run(["git", "add", INDEX_FILE], check=True)

    # চেক যদি সত্যিই কোনো পরিবর্তন থাকে
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"], capture_output=True)
    if diff.returncode != 0:
        subprocess.run(["git", "commit", "-m", "Update last index"], check=True)
        
        # রিমোটের নতুন পরিবর্তন টেনে রিবেজ করে পুশ
        subprocess.run(["git", "pull", "--rebase", "origin", "main"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("✅ Index committed and pushed")
    else:
        print("ℹ️  No change in index")
except subprocess.CalledProcessError as e:
    print(f"⚠️ Git error (push may have failed): {e}")
