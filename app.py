import os
import openai
from flask import Flask, jsonify, request

app = Flask(__name__)

# ดึง API Key จาก Environment Variables
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/generate_prompt/<category>', methods=['GET'])
def generate_prompt(category):
    model_type = request.args.get('model', 'Runway')  # เลือก Runway หรือ Kling
    lang = request.args.get('lang', 'en')  # ภาษา (en/th)
    temperature = float(request.args.get('temperature', 0.7))  # ปรับความคิดสร้างสรรค์
    max_tokens = int(request.args.get('max_tokens', 300))  # กำหนดความยาวของ prompt

    response = openai.chat.completions.create(  # ใช้เวอร์ชันใหม่!
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an AI prompt generator specialized in AI video generation."},
            {"role": "user", "content": f"Generate a detailed prompt for {category} in {lang}"}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return jsonify({"prompt": response.choices[0].message.content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
