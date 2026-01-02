from flask import Flask, jsonify
import subprocess
import shutil

app = Flask(__name__)

@app.route("/")
def home():
    return "FFmpeg check service is running"

@app.route("/check-ffmpeg")
def check_ffmpeg():
    # Method 1: check if ffmpeg is in PATH
    ffmpeg_path = shutil.which("ffmpeg")

    if not ffmpeg_path:
        return jsonify({
            "ffmpeg_found": False,
            "message": "FFmpeg not found in PATH"
        })

    # Method 2: try running ffmpeg -version
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )

        return jsonify({
            "ffmpeg_found": True,
            "ffmpeg_path": ffmpeg_path,
            "ffmpeg_output": result.stdout.split("\n")[0]
        })

    except Exception as e:
        return jsonify({
            "ffmpeg_found": False,
            "error": str(e)
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
