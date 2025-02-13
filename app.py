import os
import openai
from flask import Flask, jsonify, request

app = Flask(__name__)

# ดึง API Key จาก Environment Variables
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/generate_prompt/<category>', methods=['GET'])
def generate_prompt(category):
    # รับค่าพารามิเตอร์จาก URL
    model_type = request.args.get('model', 'Runway')  # Runway หรือ Kling
    lang = request.args.get('lang', 'en')  # เลือกภาษา (en/th)
    temperature = float(request.args.get('temperature', 0.7))  # ความคิดสร้างสรรค์ (0.0 - 1.0)
    max_tokens = int(request.args.get('max_tokens', 300))  # ความยาวของ prompt

    # ตรวจสอบว่า model ถูกต้องไหม
    if model_type not in ["Runway", "Kling"]:
        return jsonify({"error": "Invalid model type. Choose 'Runway' or 'Kling'."})

    # กำหนด system prompt ตาม model
    system_prompt = f"You are an expert in generating high-quality AI video prompts for {model_type}."
    if lang == "th":
        system_prompt = f"คุณเป็นผู้เชี่ยวชาญในการสร้างคำสั่ง AI วิดีโอที่สมจริงและละเอียดสูงสำหรับ {model_type}."

    # คำสั่งที่เหมาะกับ AI Video Generator
    user_prompt = f"""
    Generate a long, structured, highly detailed AI video prompt for {category} in {model_type} format.
    Include elements such as motion style, camera movement, resolution, lighting, cinematic tone, and dynamic effects.
    """

    # ขอให้ OpenAI สร้าง prompt
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )

    # จัดโครงสร้าง JSON ให้เหมาะกับ API
    response_json = {
        "category": category,
        "model": model_type,
        "language": "Thai" if lang == "th" else "English",
        "prompt": response['choices'][0]['message']['content']
    }

    return jsonify(response_json)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
