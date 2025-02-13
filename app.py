import os
import openai
from flask import Flask, jsonify, request

app = Flask(__name__)

# ดึง API Key จาก Environment Variables
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/generate_prompt/<category>', methods=['GET'])
def generate_prompt(category):
    model_type = request.args.get('model', 'Runway')  # เลือก Runway หรือ Kling
    lang = request.args.get('lang', 'en')  # ภาษา en หรือ th
    temperature = float(request.args.get('temperature', 0.7))
    max_tokens = int(request.args.get('max_tokens', 300))

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an AI trained to generate high-quality video prompts."},
            {"role": "user", "content": f"Generate a professional video prompt for {category} in {model_type}. Keep it structured, cinematic, and detailed."}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )

    english_prompt = response['choices'][0]['message']['content']

    # สร้างคำอธิบายภาษาไทย
    thai_response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an AI translator. Translate the given video prompt to Thai in a detailed, human-friendly way."},
            {"role": "user", "content": f"Translate this video prompt to Thai:\n\n{english_prompt}"}
        ],
        temperature=0.5,
        max_tokens=max_tokens
    )

    thai_description = thai_response['choices'][0]['message']['content']

    return jsonify({
        "prompt": english_prompt,
        "thai_description": thai_description
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
