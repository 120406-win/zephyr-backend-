from flask import Flask, request, jsonify
import base64
from openai import OpenAI
import os

app = Flask(__name__)

MIMO_KEY = os.environ.get("MIMO_KEY", "")
VOICE_AUDIO_B64 = os.environ.get("VOICE_AUDIO_B64", "")

@app.route("/tts", methods=["POST"])
def tts():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "no text"}), 400
    try:
        client = OpenAI(
            api_key=MIMO_KEY,
            base_url="https://api.xiaomimimo.com/v1",
        )
        completion = client.chat.completions.create(
            model="mimo-v2.5-tts-voiceclone",
            messages=[
                {"role": "user", "content": text},
                {"role": "assistant", "content": text}
            ],
            audio={
                "format": "wav",
                "voice": f"data:audio/wav;base64,{VOICE_AUDIO_B64}"
            }
        )
        message = completion.choices[0].message
        audio_b64 = message.audio.data
        return jsonify({"audio": audio_b64})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def index():
    return "Zephyr Backend OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
