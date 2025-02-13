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
    temperature = float(request.args.get('temperature', 0.7))  # ค่าความคิดสร้างสรรค์ (0.0 - 1.0)
    max_tokens = int(request.args.get('max_tokens', 300))  # ความยาวของ prompt

    prompt_text = f"""
    Generate a highly detailed AI Video prompt in {category} for {model_type}. 
    - Describe the scene setting, atmosphere, and lighting.
    - Provide details on camera movement and cinematographic composition.
    - Include environmental elements like fog, fireflies, or cyberpunk neon lights.
    - Avoid using Markdown, bullet points, or section headers.
    """

    client = openai.OpenAI()  # ✅ เวอร์ชันใหม่ต้องใช้ OpenAI Client

    response = client.chat.completions.create(  # ✅ เวอร์ชันใหม่ใช้ `client.chat.completions.create()`
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an AI prompt generator specialized in AI Video generation."},
            {"role": "user", "content": prompt_text}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )

    return jsonify({"prompt": response.choices[0].message.content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
