import os
import openai
from flask import Flask, jsonify, request

app = Flask(__name__)

# ใช้ API Key จาก Environment Variables
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/generate_prompt/<category>', methods=['GET'])
def generate_prompt(category):
    try:
        # รับค่าจาก URL
        model_type = request.args.get('model', 'Runway')  # เลือกโมเดล Runway หรือ Kling
        lang = request.args.get('lang', 'en')  # ภาษา (en/th)
        temperature = float(request.args.get('temperature', 0.7))  # ความคิดสร้างสรรค์ (0.0 - 1.0)
        max_tokens = int(request.args.get('max_tokens', 300))  # ความยาวของ prompt

        # ตรวจสอบว่า model และ prompt มีค่าหรือไม่
        if not model_type:
            return jsonify({"error": "Missing required argument: 'model'"}), 400

        # ข้อความที่ใช้ให้ GPT สร้าง Prompt
        prompt_text = f"""
        Generate a highly detailed AI video prompt for {category} in {model_type}.
        The prompt should include:
        - Scene composition
        - Lighting & Atmosphere
        - Cinematic effects
        - Camera movements
        - Aspect ratio, resolution, and frame rate
        """

        # เรียกใช้ OpenAI API
        response = client.chat.completions.create(
            model="gpt-4-turbo",  # ระบุโมเดลที่ต้องการใช้
            messages=[
                {"role": "system", "content": "You are an AI video prompt generator for cinematic AI models."},
                {"role": "user", "content": prompt_text}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )

        # ดึงผลลัพธ์ที่ AI สร้างขึ้น
        ai_generated_prompt = response.choices[0].message.content.strip()

        # แปลเป็นภาษาไทย ถ้าผู้ใช้เลือกภาษา "th"
        thai_translation = ""
        if lang == "th":
            thai_translation = translate_to_thai(ai_generated_prompt)

        # ส่งผลลัพธ์กลับไป
        return jsonify({
            "English Prompt for AI": ai_generated_prompt,
            "Thai Explanation for Humans": thai_translation
        }), 200, {'Content-Type': 'application/json; charset=utf-8'}

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # ส่ง Error ถ้ามีปัญหา

def translate_to_thai(text):
    """ ฟังก์ชันแปลภาษาอังกฤษเป็นไทย """
    return f"🔹 คำอธิบายภาษาไทย: {text}"  # สามารถใช้ Google Translate API ได้ถ้าต้องการ

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)  # ใช้ Port 10000 ตามที่ตั้งค่าไว้
