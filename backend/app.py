import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Store chatbots in memory (simple version)
chatbots = {}

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

@app.route('/api/initialize', methods=['POST'])
def initialize():
    data = request.json
    company_id = data.get('company_id')
    chatbots[company_id] = {
        'name': data.get('company_name'),
        'industry': data.get('industry'),
        'messages': []
    }
    return jsonify({"status": "success", "company_id": company_id})

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    company_id = data.get('company_id')
    query = data.get('query')
    
    # Simple OpenAI call
    import openai
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"You are EcoQuery, a sustainability assistant. Help users understand environmental commitments and ESG goals. Be specific and helpful."
                },
                {"role": "user", "content": query}
            ],
            max_tokens=300
        )
        
        answer = response.choices[0].message.content
        
        return jsonify({
            "response": answer,
            "timestamp": "2025-11-14"
        })
    except Exception as e:
        return jsonify({
            "response": "I'm having trouble connecting. Please try again.",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
