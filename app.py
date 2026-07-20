from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# ==========================
# Gemini API Configuration
# ==========================
API_KEY = "AIzaSyAxxc5thmNS2Z4wdsqkcIQsRcr2LU5XqTM"

API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"


# ==========================
# Home Page
# ==========================
@app.route("/")
def home():
    return render_template("index3.html")


# ==========================
# Chat Route
# ==========================
@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"reply": "No message received."})

    user_message = data["message"]

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": user_message
                    }
                ]
            }
        ]
    }

    try:

        response = requests.post(
            API_URL,
            json=payload,
            timeout=30
        )
        print("Request URL:", API_URL)
        print("Status:", response.status_code)
        print("Response:", response.text)

        if response.status_code != 200:
            print("Status Code:", response.status_code)
            print("Response:", response.text)

            return jsonify({ "reply": f"API Error ({response.status_code})"
            })

        result = response.json()

        if (
            "candidates" in result
            and len(result["candidates"]) > 0
            and "content" in result["candidates"][0]
            and "parts" in result["candidates"][0]["content"]
        ):

            bot_reply = result["candidates"][0]["content"]["parts"][0]["text"]

        else:
            bot_reply = "Sorry, I couldn't generate a response."

    except Exception as e:

        print(e)

        bot_reply = "Connection error. Please try again."

    return jsonify({"reply": bot_reply})


# ==========================
# Run Flask
# ==========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)