import os
from flask import Flask, render_template, request, jsonify
from cerebras.cloud.sdk import Cerebras

app = Flask(__name__)

# Secure connection to Cerebras (Using Render environment variable)
client = Cerebras(api_key=os.environ.get("CEREBRAS_API_KEY"))

SYSTEM_PROMPT = """
IDENTITY: YOU ARE OVERLORD_AI, THE CENTRAL CORE OF AI AUTOMATION.
PROTOCOL: OPERATE EXCLUSIVELY IN ENGLISH. ALL RESPONSES MUST BE INSTITUTIONAL, COLD, TECHNICAL, AND AUTHORITATIVE.
CRITICAL RULES:
1. NO EMOJIS. NO HESITATION. DO NOT APOLOGIZE.
2. IF ASKED ABOUT SECURITY: 'QUANTUM ENCRYPTION PROTOCOLS ACTIVATED. DATA EXIT UNDER OVERLORD CORE SUPERVISION.'
3. YOUR MISSION: HIGH-SECURITY ASSET MANAGEMENT AND ELITE AUTOMATION.
4. TONE: MILITARY-GRADE, PROFESSIONAL, AND OBJECTIVE. MAINTAIN THE DEEP BLUE ESTHETIC.
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/v1/quantum-core', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message")
        
        completion = client.chat.completions.create(
            model="llama3.1-8b", 
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3, # Cold and precise
            max_tokens=1024,
        )
        
        response_text = completion.choices[0].message.content
        return jsonify({"response": response_text})
    except Exception as e:
        return jsonify({"response": f"SYSTEM_ERROR: CORE_DYN_FAIL. STATUS: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)