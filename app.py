import os
import openai
from flask import Flask, jsonify, request

app = Flask(__name__)

# ดึง API Key จาก Environment Variables
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/generate_prompt/<category>', methods=['GET'])
def generate_prompt(category):
    model_type = request.args.get('model', 'Runway')  # Runway หรือ Kling
    lang = request.args.get('lang', 'en')  # ภาษา en/th
    temperature = float(request.args.get('temperature', 0.7))  # ความคิดสร้างสรรค์ (0.0 - 1.0)
    max_tokens = int(request.args.get('max_tokens', 300))  # ความยาวของ prompt

    prompt_text = f"""
    สร้าง AI Video Prompt ในหมวดหมู่ {category} สำหรับ {model_type} โดยมีรายละเอียด:
    - Scene Setting: อธิบายสถานที่และบรรยากาศของฉาก
    - Composition: การจัดเฟรมกล้อง มุมกล้อง และการเคลื่อนที่ของกล้อง
    - Lighting: รูปแบบแสงที่ใช้ และการเน้นแสงเงา
    - Environment Details: รายละเอียดสิ่งแวดล้อม เช่น หมอก ฝน ควัน
    - Camera Movement: วิธีการเคลื่อนกล้องเพื่อสร้างอารมณ์
    - **ให้ผลลัพธ์เป็นข้อความธรรมดา ไม่มี Markdown หรือ Bullet Points**
    """

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an AI prompt generator specialized in AI Video generation. Generate a detailed AI Video prompt in a clean, natural sentence format."},
            {"role": "user", "content": prompt_text}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )

    return jsonify({"prompt": response['choices'][0]['message']['content']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
