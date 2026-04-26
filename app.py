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
    
    api_key = os.environ.get("OPENROUTER_API_KEY")
    
    if not api_key:
        return jsonify({"error": "API key not found"}), 500
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://labmind.railway.app",
                "X-Title": "LabMind AI"
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
            },
            timeout=30
        )
        
        data = response.json()
        print(data)
        if "choices" not in data:
            return jsonify({"error": str(data)}), 500
            
        result = data["choices"][0]["message"]["content"]
        return jsonify({"result": result})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)