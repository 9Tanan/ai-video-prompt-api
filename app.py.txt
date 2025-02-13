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

base_prompts = {
    "Cinematic AI": ["A futuristic cyberpunk city with neon lights, raining, cinematic atmosphere"],
    "Abstract AI Motion Graphics": ["A seamless looping background of glowing light particles moving in a dark space"],
    "Nature & Surreal": ["A magical enchanted forest with glowing trees and mystical creatures"],
    "Business & Technology": ["A modern corporate office with AI holographic displays, futuristic design"],
    "วิดีโอสต็อกแบบ 4K": ["A stunning 4K landscape video with breathtaking visuals"],
    "วิดีโอแนวตั้ง": ["A vertical video optimized for mobile viewing with smooth transitions"],
    "ธีมเพลตวิดีโอ": ["A pre-designed video template with customizable elements"],
    "เพลงสต็อก": ["A stock music video with smooth and relaxing beats"],
    "พื้นหลังวิดีโอ": ["An abstract moving background with neon waves"],
    "ภาพเคลื่อนไหว": ["A 2D animated explainer video with modern graphics"],
    "เอฟเฟกต์วิดีโอ": ["A video with stunning visual effects and cinematic transitions"],
    "ฉากเขียว (Green Screen)": ["A dynamic green screen background for virtual production"]
}

# ฟังก์ชันสุ่มหมวดหมู่ใหม่ ถ้าผู้ใช้พิมพ์คำที่ไม่มีอยู่ในระบบ
def generate_prompt(category):
    if category in trending_keywords:
        selected_keyword = random.choice(trending_keywords[category])
        prompt = f"{random.choice(base_prompts[category])}, highly detailed, trending on Adobe Stock, {selected_keyword}"
    else:
        # ถ้าหมวดหมู่ไม่มีในระบบ ให้ GPT สร้างหมวดหมู่ใหม่แบบใกล้เคียง
        new_category = random.choice(list(trending_keywords.keys()))
        selected_keyword = random.choice(trending_keywords[new_category])
        prompt = f"[Custom Category: {category}] {random.choice(base_prompts[new_category])}, highly detailed, trending on Adobe Stock, {selected_keyword}"
    return prompt

# API route
@app.route('/get_prompt/<category>', methods=['GET'])
def get_prompt(category):
    return jsonify({"prompt": generate_prompt(category)})

# Run API
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
