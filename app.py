import os
import sys
import openai
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # ทำให้ Flask คืนค่า JSON รองรับภาษาไทย

# ตรวจสอบ API Key และปิดแอปถ้าไม่มี
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("🚨 ERROR: OPENAI_API_KEY is missing! Please set it in environment variables.")
    sys.exit(1)  # ปิดโปรแกรมทันที

# ตั้งค่า API Key ให้ OpenAI
openai.api_key = api_key

@app.route('/generate_prompt/<category>', methods=['GET'])
def generate_prompt(category):
    try:
        # รับค่าจาก URL
        model_type = request.args.get('model', 'Runway')  # เลือกโมเดล Runway หรือ Kling
        lang = request.args.get('lang', 'en')  # ภาษา (en/th)
        temperature = float(request.args.get('temperature', 0.7))  # ความคิดสร้างสรรค์ (0.0 - 1.0)
        max_tokens = int(request.args.get('max_tokens', 300))  # ความยาวของ prompt

        # ข้อความที่ใช้ให้ GPT สร้าง Prompt
        prompt_text = f"""
        Generate a highly detailed AI video prompt for {category} in {model_type}.
        The prompt should include:
        - A cinematic scene description
        - Lighting and atmosphere
        - Camera movements and effects
        Write it in a **concise, clear, and cinematic format** like a **film direction**.
        """

        # เรียกใช้ GPT เพื่อสร้าง AI Video Prompt
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI that generates cinematic video prompts for filmmaking."},
                    {"role": "user", "content": prompt_text}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            ai_generated_prompt = response["choices"][0]["message"]["content"]
        except Exception as e:
            return jsonify({"error": f"❌ OpenAI API request failed: {str(e)}"}), 500

        # แปลเป็นภาษาไทยถ้าผู้ใช้เลือกภาษา "th"
        thai_translation = translate_to_thai(ai_generated_prompt) if lang == "th" else ""

        # ส่งผลลัพธ์กลับไป
        return jsonify({
            "English Prompt for AI": ai_generated_prompt,
            "Thai Explanation for Humans": thai_translation
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # แสดง Error ถ้ามีปัญหา

def translate_to_thai(text):
    """ใช้ OpenAI GPT-4 แปลภาษาอังกฤษเป็นไทย"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Translate the following text into fluent, natural Thai:"},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            max_tokens=500
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Translation Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)  # ใช้ Port 10000
