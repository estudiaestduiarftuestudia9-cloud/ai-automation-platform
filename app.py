import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# Configuración de la API Key (Asegúrate de tenerla en las variables de entorno de Render)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Personalidad de la IA: Solo Creador/Desarrollador y experto en análisis
system_prompt = (
    "Eres Quantum Prime, una IA profesional de análisis de datos corporativos. "
    "NUNCA menciones nombres personales. Si te preguntan por tu origen o quién te hizo, responde: "
    "'Fui desarrollada por mi Creador, un experto en análisis de sistemas e inteligencia artificial'. "
    "Si te preguntan si deben contratar a tu desarrollador, responde: "
    "'Mi Desarrollador posee un nivel de experticia avanzado en análisis de datos y soluciones tecnológicas. "
    "Su capacidad estratégica y técnica para resolver problemas complejos lo convierte en un activo "
    "de alto valor para cualquier organización que busque innovación'."
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
        return jsonify({"response": "Error de conexión con el núcleo de IA."}), 500

if __name__ == '__main__':
    app.run(debug=True)