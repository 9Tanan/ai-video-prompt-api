import os
import sys
import openai
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # รองรับภาษาไทยใน JSON

# ตรวจสอบ API Key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("🚨 ERROR: OPENAI_API_KEY is missing! Please set it in environment variables.")
    sys.exit(1)

# ตั้งค่า OpenAI Client
client = openai.OpenAI(api_key=api_key)

@app.route('/generate_prompt/<category>', methods=['GET'])
def generate_prompt(category):
    try:
        model_type = request.args.get('model', 'Runway')
        lang = request.args.get('lang', 'en')
        temperature = float(request.args.get('temperature', 0.7))
        max_tokens = int(request.args.get('max_tokens', 300))

        prompt_text = f"""
        Generate a highly detailed AI video prompt for {category} in {model_type}.
        The prompt should include:
        - A cinematic scene description
        - Lighting and atmosphere
        - Camera movements and effects
        Write it in a **concise, clear, and cinematic format** like a **film direction**.
        """

        # เรียก OpenAI API
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an AI that generates cinematic video prompts for filmmaking."},
                {"role": "user", "content": prompt_text}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )

        ai_generated_prompt = response.choices[0].message.content

        # แปลเป็นภาษาไทย
        thai_translation = translate_to_thai(ai_generated_prompt) if lang == "th" else ""

        return jsonify({
            "English Prompt for AI": ai_generated_prompt,
            "Thai Explanation for Humans": thai_translation
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def translate_to_thai(text):
    """ แปลและจัดรูปแบบภาษาไทยให้อ่านง่ายขึ้น """
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Translate the following text into fluent, natural Thai with proper line breaks:"},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            max_tokens=500
        )
        translated_text = response.choices[0].message.content

        # จัดรูปแบบภาษาไทยให้มีบรรทัดเว้นวรรค
        formatted_text = translated_text.replace(".", ".\n\n")  # เว้นวรรคเพิ่มให้อ่านง่าย
        return formatted_text

    except Exception as e:
        return f"⚠️ Translation Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)  
