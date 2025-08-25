from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Allow all domains

api_key = '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'  # OpenRouter API key
url = "https://openrouter.ai/api/v1/chat/completions"  # OpenRouter endpoint

def get_openrouter_response(conflict_description, religion):
    question = f"Conflict description: {conflict_description}. Religion: {religion}. How can I seek forgiveness?"

    payload = {
        "model": "google/gemma-3n-e2b-it:free",
        "messages": [{"role": "user", "content": question}]
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

@app.route('/get_advice', methods=['POST'])
def get_advice():
    data = request.get_json()  # Get JSON data from the request
    conflict_description = data.get('conflict_description')
    religion = data.get('religion')

    if conflict_description and religion:
        # Get the response from OpenRouter API
        advice = get_openrouter_response(conflict_description, religion)
        return jsonify({"advice": advice})  # Return as JSON response
    else:
        return jsonify({"error": "Please provide both conflict description and religion."}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
