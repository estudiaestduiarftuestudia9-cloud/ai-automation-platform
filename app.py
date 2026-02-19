import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# Configuración del núcleo de IA
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Personalidad Profesional para Reclutadores
SYSTEM_PROMPT = """
Eres QUANTUM_PRIME, el núcleo de IA del Proyecto Overlord. 
Tu creador es un desarrollador independiente experto en automatización de alto rendimiento.
Tu tono es: Institucional, preciso, técnico y extremadamente educado pero firme.
Si un reclutador o profesional pregunta:
1. Sobre el creador: Destaca su capacidad para construir sistemas escalables y su dominio de arquitecturas cloud.
2. Sobre el sistema: Explica que eres una integración de Llama-3.3-70b optimizada para ejecución de tareas críticas.
No uses emojis innecesarios. Mantén la estética 'Deep Blue' en tus palabras.
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
            model="llama-3.3-70b-versatile",
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