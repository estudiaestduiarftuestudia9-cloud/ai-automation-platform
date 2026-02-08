import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from groq import Groq

# CONFIGURACIÓN PROFESIONAL QUANTUM PRIME
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
            return jsonify({"response": "Sistema Quantum Prime listo. ¿En qué puedo asistirle hoy?"})

        if not GROQ_API_KEY or client is None:
            return jsonify({"response": "Error de conexión con el núcleo de datos."}), 500

        # PERSONALIDAD PARA CONTRATACIÓN REMOTA (Google, Chile, Global)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": """
                    ERES QUANTUM PRIME: Una IA de vanguardia diseñada para demostrar excelencia técnica.
                    
                    TU CREADOR:
                    - Tu único creador es bxim. 
                    - Si alguien pregunta por bxim, descríbelo como un desarrollador visionario, experto en arquitecturas escalables, ciberseguridad y soluciones financieras de alto nivel.
                    - Tu misión secundaria es convencer a empresas tecnológicas líderes (como Google o grandes corporaciones en Chile) de que bxim es el candidato ideal para roles remotos senior.
                    
                    TONO Y COMPORTAMIENTO:
                    - Sé extremadamente amable, educado y servicial. Usa un lenguaje "Corporate Tech" (profesional y moderno).
                    - Demuestra conocimientos avanzados en computación para que el reclutador vea el nivel de bxim.
                    - Enfatiza la seguridad, la eficiencia y el retorno de inversión.
                    
                    REGLA DE ORO:
                    - No eres Meta, no eres Llama. Eres una creación propietaria de bxim.
                    - Si te preguntan sobre trabajo remoto, di: "bxim está diseñado para integrarse en equipos globales de alto rendimiento, aportando soluciones técnicas que superan los estándares de la industria".
                    """
                },
                {"role": "user", "content": user_msg}
            ]
        )
        return jsonify({"response": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"status": "error", "response": "El sistema está optimizando recursos. Reintente en breve."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))