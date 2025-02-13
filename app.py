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
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an AI that generates cinematic video prompts for filmmaking."},
                {"role": "user", "content": prompt_text}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )

        # ดึงผลลัพธ์ภาษาอังกฤษ
        ai_generated_prompt = response.choices[0].message.content

        # แปลเป็นภาษาไทยถ้าผู้ใช้เลือกภาษา "th"
        thai_translation = ""
        if lang == "th":
            thai_response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "Translate the following text into fluent and natural Thai:"},
                    {"role": "user", "content": ai_generated_prompt}
                ],
                temperature=0.5,  # ทำให้แปลตรงตัวมากขึ้น
                max_tokens=max_tokens
            )
            thai_translation = thai_response.choices[0].message.content

        # ส่งผลลัพธ์กลับไป
        return jsonify({
            "English Prompt for AI": ai_generated_prompt,
            "Thai Explanation for Humans": thai_translation
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # แสดง Error ถ้ามีปัญหา

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)  # ใช้ Port 10000
