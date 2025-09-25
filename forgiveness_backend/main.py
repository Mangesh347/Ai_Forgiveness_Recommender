
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import requests
# import re
# import os

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# # ---- CONFIG ----
# API_KEY = os.getenv(
#     "OPENROUTER_KEY",
#     "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",
# )
# URL = "https://openrouter.ai/api/v1/chat/completions"

# # In-memory DB { email: {"username":..., "password":..., "history": [...] } }
# users = {}

# RELIGION_LANG = {
#     "Hinduism": "any",
#     "Christianity": "any",
#     "Islam": "any",
#     "Buddhism": "any",
#     "Sikhism": "any",
#     "Judaism": "any",
#     "Baháʼí Faith": "any",
#     "Jainism": "any",
#     "Shinto": "any",
#     "Taoism / Daoism": "any",
# }

# # ---- UTILITIES ----
# def clean_response(text: str) -> str:
#     if not text:
#         return "No advice received."
#     text = re.sub(r"◁think▷.*?◁/think▷", "", text, flags=re.DOTALL)
#     text = re.sub(r"\$\s*\d+\s*:", "", text)
#     text = re.sub(r"^\s*[\d]+\s*[:.]\s*", "", text, flags=re.MULTILINE)
#     text = text.replace("$", "")
#     text = re.sub(r"\n{2,}", "\n", text)
#     text = text.strip()
#     # remove any non-ASCII to enforce transliteration
#     text = re.sub(r"[^\x00-\x7F]+", "", text)
#     return text.strip()

# def get_openrouter_response(conflict_description, religion, user_message=None):
#     """
#     Generate AI response in same language (transliterated),
#     casual + forgiveness tone, no switching to English.
#     """
#     if not user_message:
#         user_message = conflict_description

#     prompt = (
#         f"You are a forgiveness guide.\n"
#         f"IMPORTANT RULES:\n"
#         f"- Detect the language user is using (Hindi, Gujarati, Marathi, Tamil, etc.)\n"
#         f"- Reply ONLY in that SAME language but written in English letters (transliteration).\n"
#         f"- Do NOT switch to English if user is not using it.\n"
#         f"- Do NOT explain in English.\n"
#         f"- Just continue naturally in user's language (transliterated).\n"
#         f"- Keep it empathetic, casual, short, and focused on forgiveness.\n\n"
#         f"Conflict: {conflict_description}\n"
#         f"User said: {user_message}\n"
#         f"Religion: {religion}\n\n"
#         f"Now reply in the SAME language (transliterated), continuing their vibe."
#     )

#     payload = {
#         "model": "z-ai/glm-4.5-air:free",
#         "messages": [{"role": "user", "content": prompt}],
#         "stream": False,
#     }
#     headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
#     try:
#         r = requests.post(URL, json=payload, headers=headers, timeout=20)
#         if r.status_code == 200:
#             data = r.json()
#             raw = data.get("choices", [{}])[0].get("message", {}).get("content", "")
#             return clean_response(raw)
#         return f"API error {r.status_code}: {r.text}"
#     except Exception as e:
#         return f"Request failed: {e}"

# # ---- ROUTES ----
# @app.route("/signup", methods=["POST"])
# def signup():
#     data = request.get_json()
#     username = data.get("username", "").strip()
#     email = data.get("email", "").strip()
#     password = data.get("password", "").strip()

#     if not username or not email or not password:
#         return jsonify({"error": "All fields are required"}), 400
#     if email in users:
#         return jsonify({"error": "Email already exists"}), 400

#     users[email] = {"username": username, "password": password, "history": []}
#     return jsonify({"message": "Signup successful"}), 200

# @app.route("/login", methods=["POST"])
# def login():
#     data = request.get_json()
#     email = data.get("email", "").strip()
#     password = data.get("password", "").strip()
#     u = users.get(email)
#     if not u or u["password"] != password:
#         return jsonify({"error": "Invalid email or password"}), 400
#     return jsonify({"username": u["username"], "email": email, "history": u["history"]})

# @app.route("/get_advice", methods=["POST"])
# def get_advice():
#     data = request.get_json()
#     email = data.get("email", "").strip()
#     conflict = data.get("conflict_description", "").strip()
#     religion = data.get("religion", "").strip()

#     if not email or email not in users:
#         return jsonify({"error": "Invalid user"}), 400

#     if not conflict:
#         return jsonify({
#             "advice": "Hello! Please describe your conflict, so I can give you forgiveness advice.",
#             "history": users[email]["history"],
#         })

#     if religion not in RELIGION_LANG:
#         return jsonify({"error": "Unsupported religion"}), 400

#     advice = get_openrouter_response(conflict, religion, user_message=conflict)

#     chat_item = {
#         "title": conflict[:25] + "...",
#         "religion": religion,
#         "messages": [
#             {"message": conflict, "sender": "user"},
#             {
#                 "message": advice,
#                 "sender": "AI",
#                 "original": advice,
#                 "currentLang": "transliterated",
#             },
#         ],
#     }
#     users[email]["history"].append(chat_item)
#     return jsonify({"advice": advice, "history": users[email]["history"]})

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)




from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# ---- CONFIG ----
API_KEY = os.getenv(
    "OPENROUTER_KEY",
    "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",
)
URL = "https://openrouter.ai/api/v1/chat/completions"

# In-memory DB { email: {"username":..., "password":..., "history": [...] } }
users = {}


RELIGION_LANG = {
    "Hinduism": "any",
    "Christianity": "any",
    "Islam": "any",
    "Buddhism": "any",
    "Sikhism": "any",
    "Judaism": "any",
    "Baháʼí Faith": "any",
    "Jainism": "any",
    "Shinto": "any",
    "Taoism / Daoism": "any",
}

# ---- UTILITIES ----
def clean_response(text: str) -> str:
    if not text:
        return "No advice received."
    text = re.sub(r"◁think▷.*?◁/think▷", "", text, flags=re.DOTALL)
    text = re.sub(r"\$\s*\d+\s*:", "", text)
    text = re.sub(r"^\s*[\d]+\s*[:.]\s*", "", text, flags=re.MULTILINE)
    text = text.replace("$", "")
    text = re.sub(r"\n{2,}", "\n", text)
    text = text.strip()
    text = re.sub(r"[^\x00-\x7F]+", "", text)
    return text.strip()

def get_openrouter_response(conflict_description, religion, user_message=None):
    """
    Generate AI response in same language (transliterated),
    empathetic forgiveness tone, with emojis and structured depth.
    """
    if not user_message:
        user_message = conflict_description

    prompt = (
        f"You are a forgiveness guide.\n\n"
        f"RULES:\n"
        f"- Detect the language user is using (Hindi, Gujarati, Marathi, Tamil, etc.).\n"
        f"- Reply ONLY in that SAME language but written in English letters (transliteration).\n"
        f"- Do NOT switch to English if user is not using it.\n"
        f"- Maintain same vibe/energy as the user (casual, empathetic, friendly).\n"
        f"- Use emojis naturally to make the response warm and supportive.\n"
        f"- If the conflict is SHORT or SIMPLE → give a medium paragraph with advice.\n"
        f"- If the conflict is LONG or COMPLEX → give:\n"
        f"   1. A short empathetic intro (1 paragraph).\n"
        f"   2. Then practical forgiveness advice in bullet/numbered points.\n"
        f"- Always keep tone supportive, non-judgmental, and focused on peace/forgiveness.\n\n"
        f"Conflict: {conflict_description}\n"
        f"User said: {user_message}\n"
        f"Religion: {religion}\n\n"
        f"Now reply in SAME language (transliterated), casual, detailed if needed, and use emojis naturally."
    )

    payload = {
        "model": "z-ai/glm-4.5-air:free",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    try:
        r = requests.post(URL, json=payload, headers=headers, timeout=20)
        if r.status_code == 200:
            data = r.json()
            raw = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            return clean_response(raw)
        return f"API error {r.status_code}: {r.text}"
    except Exception as e:
        return f"Request failed: {e}"

# ---- ROUTES ----
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400
    if email in users:
        return jsonify({"error": "Email already exists"}), 400

    users[email] = {"username": username, "password": password, "history": []}
    return jsonify({"message": "Signup successful"}), 200

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    u = users.get(email)
    if not u or u["password"] != password:
        return jsonify({"error": "Invalid email or password"}), 400
    return jsonify({"username": u["username"], "email": email, "history": u["history"]})

@app.route("/get_advice", methods=["POST"])
def get_advice():
    data = request.get_json()
    email = data.get("email", "").strip()
    conflict = data.get("conflict_description", "").strip()
    religion = data.get("religion", "").strip()

    if not email or email not in users:
        return jsonify({"error": "Invalid user"}), 400

    if not conflict:
        return jsonify({
            "advice": "Hello! Please describe your conflict, so I can give you forgiveness advice.",
            "history": users[email]["history"],
        })

    if religion not in RELIGION_LANG:
        return jsonify({"error": "Unsupported religion"}), 400

    advice = get_openrouter_response(conflict, religion, user_message=conflict)

    chat_item = {
        "title": conflict[:25] + "...",
        "religion": religion,
        "messages": [
            {"message": conflict, "sender": "user"},
            {
                "message": advice,
                "sender": "AI",
                "original": advice,
                "currentLang": "transliterated",
            },
        ],
    }
    users[email]["history"].append(chat_item)
    return jsonify({"advice": advice, "history": users[email]["history"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
