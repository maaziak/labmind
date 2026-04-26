from flask import Flask, render_template, request, jsonify
import requests
import os


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    hypothesis = request.json.get("hypothesis", "")
    
    print("API KEY:", os.environ.get('OPENROUTER_API_KEY', 'NOT_FOUND'))
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY', 'NOT_FOUND')}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openrouter/free",
            "messages": [
                {
                    "role": "user",
                    "content": f"""You are an expert scientific lab assistant. Given the hypothesis below, generate a complete, realistic experiment plan.

Hypothesis: {hypothesis}

Respond in this exact format:

## 🔬 Protocol Steps
(numbered step-by-step lab procedure)

## 🧪 Reagents & Estimated Costs
(table of materials needed with USD cost estimates)

## 📅 Week-by-Week Timeline
(realistic timeline a real lab would follow)

## ⚠️ Safety Warnings
(important safety considerations)

## 📋 PI Summary
(2-3 sentence executive summary a Principal Investigator could hand to their team Monday morning)"""
                }
            ]
        }
    )
    print(response.json())  # Debugging line to check the API response
    result = response.json()["choices"][0]["message"]["content"]
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))