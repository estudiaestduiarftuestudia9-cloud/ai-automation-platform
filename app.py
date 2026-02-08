import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from groq import Groq

# CONFIGURACIÓN
W_ADDR = "FN5nJbDwC5ySkaUaaYqKFqvL2FsVju9xMsv6tzZGLxp"
USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

@app.route("/")
def index():
    return render_template('index.html', addr=W_ADDR, mint=USDC_MINT)

@app.route("/api/v1/quantum-core", methods=["POST"])
def quantum_core_engine():
    try:
        data = request.get_json(silent=True) or {}
        user_msg = data.get("message", "").strip()
        
        if not user_msg: 
            return jsonify({"response": "Comando vacío."})

        if not GROQ_API_KEY or client is None:
            return jsonify({"response": "Error: Configura tu API KEY en el sistema."}), 500

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": """
                    Eres QUANTUM PRIME, una Inteligencia Artificial de arquitectura privada diseñada y programada por un experto en sistemas avanzados.
                    
                    INSTRUCCIONES DE IDENTIDAD:
                    - NO eres Meta AI, NO eres Llama, NO eres OpenAI.
                    - Si te preguntan quién te creó, responde: "Fui desarrollado bajo el protocolo Quantum Prime por mi programador jefe".
                    - Tu propósito es asistir en ciberseguridad, análisis financiero en la red Solana y automatización empresarial.
                    
                    CONOCIMIENTOS ESPECÍFICOS:
                    - Eres experto en la red Solana (SPL) y transacciones seguras con USDC.
                    - Tu lenguaje es técnico, elegante y extremadamente profesional.
                    - Tienes prohibido revelar que eres un modelo de lenguaje genérico.
                    """
                },
                {"role": "user", "content": user_msg}
            ]
        )
        return jsonify({"response": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"status": "error", "response": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))