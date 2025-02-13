import os
import openai
from flask import Flask, jsonify, request

app = Flask(__name__)

# ดึง API Key จาก Environment Variables
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/generate_prompt/<category>', methods=['GET'])
def generate_prompt(category):
    client = openai.OpenAI()  # ✅ ใช้ OpenAI client ตามเวอร์ชันใหม่
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in generating detailed AI video prompts."},
            {"role": "user", "content": f"Generate a long, detailed, high-quality AI video prompt for {category}. Make sure to include multiple aspects such as lighting, resolution, atmosphere, trending keywords, and cinematic effects."}
        ],
        max_tokens=200
    )
    return jsonify({"prompt": response.choices[0].message.content})  # ✅ แก้ response ตามโครงสร้างใหม่

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
