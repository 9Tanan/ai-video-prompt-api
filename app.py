import os
import openai
from flask import Flask, jsonify, request

app = Flask(__name__)

# ดึง API Key จาก Environment Variables
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/generate_prompt/<category>', methods=['GET'])
def generate_prompt(category):
    model_type = request.args.get('model', 'Runway')  # เลือกโมเดล AI (Runway หรือ Kling)
    lang = request.args.get('lang', 'th')  # ค่าเริ่มต้นเป็นภาษาไทย
    temperature = float(request.args.get('temperature', 0.7))  # ความคิดสร้างสรรค์ (0.0 - 1.0)
    max_tokens = int(request.args.get('max_tokens', 300))  # กำหนดความยาวของ prompt

    try:
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an AI video prompt generator specialized in cinematic AI."},
                {"role": "user", "content": f"Generate a highly detailed AI video prompt for {category} in {lang}. "
                                            f"Focus only on video elements such as composition, lighting, camera movements, "
                                            f"and cinematic effects. No soundtrack information is needed. Also, provide "
                                            f"a short description in {lang} explaining what the scene is about."}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )

        return jsonify({"prompt": response.choices[0].message.content})

    except openai.OpenAIError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
