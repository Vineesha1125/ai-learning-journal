from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables (safe locally; ignored on Render)
load_dotenv()

app = Flask(__name__)

# In-memory storage
notes = []

# ✅ SAFE CLIENT CREATION
def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")
    return genai.Client(api_key=api_key)


def generate_summary(note_text):
    try:
        client = get_gemini_client()

        prompt = f"""You are a learning assistant. Summarize this learning note in one concise sentence (max 15 words).
        
Learning Note: {note_text}

Summary:"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()

    except Exception as e:
        return f"Error generating summary: {str(e)}"


def generate_insights(all_notes):
    try:
        client = get_gemini_client()

        notes_text = "\n".join([f"- {note['text']}" for note in all_notes])

        prompt = f"""You are a learning coach. Based on these learning notes, provide:
1. Key patterns or themes (2-3 sentences)
2. One actionable suggestion for what to learn next

Learning Notes:
{notes_text}

Insights:"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()

    except Exception as e:
        return f"Error generating insights: {str(e)}"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add_note", methods=["POST"])
def add_note():
    data = request.json
    note_text = data.get("note", "")

    if not note_text:
        return jsonify({"error": "Note cannot be empty"}), 400

    summary = generate_summary(note_text)

    note = {
        "id": len(notes) + 1,
        "text": note_text,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "summary": summary
    }

    notes.append(note)

    return jsonify({
        "success": True,
        "note": note,
        "message": "Note added with AI summary!"
    })


@app.route("/get_notes", methods=["GET"])
def get_notes():
    return jsonify({"notes": notes})


@app.route("/get_insights", methods=["GET"])
def get_insights():
    if not notes:
        return jsonify({
            "success": False,
            "message": "Add some notes first to get insights!"
        })

    insights = generate_insights(notes)

    return jsonify({
        "success": True,
        "insights": insights,
        "total_notes": len(notes)
    })


@app.route("/test_ai", methods=["GET"])
def test_ai():
    try:
        client = get_gemini_client()

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Say 'AI is working!' in a friendly way"
        )

        return jsonify({
            "success": True,
            "response": response.text
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    print("🚀 Starting AI Learning Journal...")
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
