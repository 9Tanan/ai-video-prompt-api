from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# หมวดหมู่ที่มีอยู่
trending_keywords = {
    "Cinematic AI": ["Cyberpunk city 4K", "Sci-fi cinematic world", "Dystopian future metropolis"],
    "Abstract AI Motion Graphics": ["Neon wave background", "Futuristic seamless loop", "Glowing abstract particles"],
    "Nature & Surreal": ["Dreamy fantasy forest", "Bioluminescent ocean", "Surreal floating island"],
    "Business & Technology": ["AI office workspace", "Holographic data analysis", "Futuristic smart city"],
    "วิดีโอสต็อกแบบ 4K": ["Ultra HD 4K video", "High-resolution cinematic"],
    "วิดีโอแนวตั้ง": ["Vertical video format", "Mobile-optimized video"],
    "ธีมเพลตวิดีโอ": ["Video templates", "Dynamic video themes"],
    "เพลงสต็อก": ["Royalty-free music", "Stock background music"],
    "พื้นหลังวิดีโอ": ["Abstract background motion", "Looping video backgrounds"],
    "ภาพเคลื่อนไหว": ["Animated motion graphics", "2D/3D animations"],
    "เอฟเฟกต์วิดีโอ": ["Special effects video", "Cinematic visual effects"],
    "ฉากเขียว (Green Screen)": ["Chroma key backgrounds", "Virtual production assets"]
}

# เพิ่มโครงสร้างที่ยาวขึ้นสำหรับ Prompt
base_prompts = {
    "Cinematic AI": [
        "A futuristic cyberpunk city with neon lights, raining, cinematic atmosphere, highly detailed, trending on Adobe Stock",
        "A dystopian futuristic cityscape filled with towering skyscrapers, holographic billboards, and neon reflections on wet streets, cinematic feel, high dynamic range"
    ],
    "Abstract AI Motion Graphics": [
        "A seamless looping animation of glowing light particles moving rhythmically in a dark space, futuristic and abstract, perfect for motion graphics",
        "A dynamic explosion of neon light waves pulsating through space, creating an immersive sci-fi digital experience, smooth transitions"
    ],
    "Nature & Surreal": [
        "A breathtaking bioluminescent ocean glowing under a starry night sky, waves crashing gently against surreal floating islands, dreamy atmosphere",
        "A mystical forest with ancient glowing trees, surreal fantasy ambiance, ultra-detailed textures and atmospheric lighting"
    ],
    "Business & Technology": [
        "A high-tech futuristic corporate office with AI-driven holographic interfaces and automated robotic assistants, professional and cutting-edge",
        "A global financial trading hub with real-time digital market charts and augmented reality projections, cinematic stock footage quality"
    ]
}

# 🔥 ฟังก์ชันสุ่มหมวดหมู่ และเพิ่มคำอธิบายให้น่าสนใจขึ้น
def generate_prompt(category):
    if category in trending_keywords:
        selected_keyword = random.choice(trending_keywords[category])
        detailed_prompt = random.choice(base_prompts[category])
        # ✅ เพิ่มคำอธิบายให้ยาวขึ้น
        prompt = f"{detailed_prompt}, realistic rendering, 4K ultra-HD, perfect for Adobe Stock, includes {selected_keyword} in a visually appealing style"
    else:
        new_category = random.choice(list(trending_keywords.keys()))
        selected_keyword = random.choice(trending_keywords[new_category])
        detailed_prompt = random.choice(base_prompts[new_category])
        # ✅ เพิ่มโครงสร้างที่อธิบายภาพได้ดีขึ้น
        prompt = f"[Custom Category: {category}] {detailed_prompt}, inspired by trending AI-generated visuals, ultra-detailed, best for cinematic stock footage, features {selected_keyword}"
    return prompt

# API Route
@app.route('/get_prompt/<category>', methods=['GET'])
def get_prompt(category):
    return jsonify({"prompt": generate_prompt(category)})

# Run API
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
