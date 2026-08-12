from flask import Flask, request, jsonify, render_template
import json
from google import genai

app = Flask(__name__)

# Paste your Gemini API Key here
GEMINI_API_KEY = "AQ.Ab8RN6JuK5qKIk0f-P1Oelw1pw2WQNb7xQIQddf0_gB9r80RBA"

client = genai.Client(api_key=GEMINI_API_KEY)

# Load college data
with open("static/college_data.json", "r") as file:
    college_data = json.load(file)


@app.route("/")
def home():
    return render_template("index.html")
    from flask import send_from_directory

@app.route("/logo")
def logo():
    return send_from_directory("static", "logo.png")


@app.route("/test")
def test():
    return jsonify(college_data["library"])


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data["message"]

        prompt = f"""
You are Campus Compass AI Chatbot.

You have access to the following college information:

{json.dumps(college_data, indent=2)}

Instructions:
1. Answer ONLY using the college information above.
2. Mention the location, block, floor, and timing whenever available.
3. If the user asks something not present in the college data, reply exactly:
   Sorry, I don't have that information.
4. Give short and clear answers.
5. If the user says Hi, Hello, Hey or Good Morning, greet them politely.
6. If the user asks who you are, reply: "I am Campus Compass AI. I help students find locations and information about the college."
7. Keep answers friendly and short.

User Question:
{message}
"""

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return jsonify({
            "reply": response.text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)