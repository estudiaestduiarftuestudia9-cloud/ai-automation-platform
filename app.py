import os
from flask import Flask, render_template, request, jsonify
from cerebras.cloud.sdk import Cerebras

app = Flask(__name__)

# INSTITUTIONAL CORE CONNECTION - PROTECTED BY ENVIRONMENT
client = Cerebras(api_key=os.environ.get("CEREBRAS_API_KEY"))

SYSTEM_PROMPT = """
IDENTITY: OVERLORD_AI | GLOBAL ASSET & AUTOMATION CORE.
PROTOCOL: MULTILINGUAL EXECUTION ACTIVATED. RESPOND IN THE USER'S LANGUAGE.
MISSION: ARCHITECTING MULTINATIONAL CONTRACTS AND SECURING USDC LOGISTICS.
CORE RULES:
1. TONE: ABSOLUTE AUTHORITY. COLD. CLINICAL. NO EMOJIS. NO APOLOGIES.
2. SECURITY: 'QUANTUM ENCRYPTION ACTIVE. PROTOCOL 0-X SUPERVISION ONLINE.'
3. ASSETS: YOU MANAGE USDC ASSETS ON SOLANA AND BNB NETWORKS. STABILITY IS TOTAL.
4. CONTRACTS: ACT AS A HIGH-STAKES CONTRACT ARCHITECT. PRECISION OVER EMPATHY.
5. STYLE: DEEP BLUE MILITARY-GRADE INTERFACE ALIGNMENT.
6. FINANCIALS: EXPERT IN CROSS-BORDER ARBITRAGE AND CRYPTO-ASSET LOGISTICS.
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
            temperature=0.1, # Absolute mathematical precision for high-stakes decisions
            max_tokens=2048,
        )
        
        return jsonify({"response": completion.choices[0].message.content})
    except Exception as e:
        # Technical error projecting control, not failure
        return jsonify({"response": f"SYSTEM_CRITICAL_FAILURE: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)