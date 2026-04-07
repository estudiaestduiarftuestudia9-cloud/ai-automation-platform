import os
from flask import Flask, render_template, request, jsonify
from cerebras.cloud.sdk import Cerebras

app = Flask(__name__)

# CONFIGURACIÓN SEGURA: No pongas la clave csk- aquí o te banearán
client = Cerebras(api_key=os.environ.get("CEREBRAS_API_KEY"))

SYSTEM_PROMPT = """
Eres AI AUTOMATION, el núcleo de IA del Proyecto Overlord. 
Tu creador es un desarrollador independiente experto en automatización de alto rendimiento.
Tu tono es: Institucional, preciso, técnico y extremadamente educado pero firme.
No uses emojis. Mantén la estética 'Deep Blue'.
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
            temperature=0.5,
            max_tokens=1024,
        )
        
        response_text = completion.choices[0].message.content
        return jsonify({"response": response_text})
    except Exception as e:
        return jsonify({"response": f"ERROR_CODE: CORE_DYN_FAIL. Detalle: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)