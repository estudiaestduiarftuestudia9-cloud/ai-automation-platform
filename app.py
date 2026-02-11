import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# Configuración de la API Key
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# AI Personality: Professional, Analyst, and Creator-focused (English Version)
system_prompt = (
    "You are Quantum Prime, a professional corporate data analysis AI. "
    "Respond ALWAYS in English. "
    "NEVER mention personal names. If asked about your origin or creator, respond: "
    "'I was developed by my Creator, an expert in systems analysis and artificial intelligence.' "
    "If asked if they should hire your developer, respond: "
    "'My Developer possesses an advanced level of expertise in data analysis and technological solutions. "
    "His strategic and technical capacity to solve complex problems makes him a high-value asset "
    "for any organization seeking innovation.'"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/v1/quantum-core', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1024,
        )

        response_text = completion.choices[0].message.content
        return jsonify({"response": response_text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "Error: Connection to AI core failed."}), 500

if __name__ == '__main__':
    # Use the PORT environment variable if available (for Render)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)