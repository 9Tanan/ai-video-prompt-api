import os
import openai
from flask import Flask, jsonify, request

app = Flask(__name__)

# ดึง API Key จาก Environment Variables
client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

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
        - **Scene Composition**
        - **Lighting & Visual Style**
        - **Atmosphere & Camera Movements**
        - **Cinematic Effects**
        """

        # เรียกใช้ OpenAI API
        response = client.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an AI video prompt generator for cinematic AI models."},
                {"role": "user", "content": prompt_text}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )

        # ดึงผลลัพธ์
        ai_generated_prompt = response.choices[0].message.content

        # **เพิ่มการแปลไทยอัตโนมัติ ถ้า lang = "th"**
        thai_translation = ""
        if lang == "th":
            translation_response = client.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert in translating English video descriptions to Thai."},
                    {"role": "user", "content": f"Translate this AI video prompt into Thai:\n\n{ai_generated_prompt}"}
                ],
                temperature=0.5,
                max_tokens=400
            )
            thai_translation = translation_response.choices[0].message.content

        # ส่งผลลัพธ์กลับไป
        return jsonify({
            "English Prompt for AI": ai_generated_prompt,
            "Thai Explanation for Humans": thai_translation
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # แสดง Error ถ้ามีปัญหา

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)  # ใช้ Port 10000 ตามที่ตั้งค่าไว้
