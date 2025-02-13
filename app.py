import os
import openai
from flask import Flask, jsonify, request

app = Flask(__name__)

# ตรวจสอบว่า API Key โหลดขึ้นมาหรือไม่
openai.api_key = os.getenv("OPENAI_API_KEY")
print("🔑 Loaded API Key:", openai.api_key)  # ดูว่า API Key โหลดได้ไหม

@app.route('/generate_prompt/<category>', methods=['GET'])
def generate_prompt(category):
    print(f"📢 Received request for category: {category}")  # Debug Request

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in generating AI video prompts."},
                {"role": "user", "content": f"Generate a detailed AI video prompt for {category}."}
            ],
            max_tokens=200
        )
        return jsonify({"prompt": response['choices'][0]['message']['content']})
    
    except Exception as e:
        print("❌ Error:", str(e))  # ดูว่าเกิด Error อะไร
        return jsonify({"error": str(e)}), 500  # ส่ง Error Response กลับไป

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
